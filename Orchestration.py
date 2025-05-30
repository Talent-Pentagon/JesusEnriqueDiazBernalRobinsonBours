import modal
import subprocess
import asyncio

app = modal.App()

# ENV VARIABLES
## Storage Paths
MODEL_DIR = "/Storage/Models"  
CLASSIFIER_DIR = "/Storage/Classifier"
BENCHMARK_DIR = "/Storage/Test"


## Model Configuration
MODELS_TO_DOWNLOAD = ["qwen3:14b"]
MODELS_TO_TEST = ["qwen3:14b"]

### Ollama version to install - you may need to update this for the latest models
OLLAMA_VERSION = "0.6.5"
### Ollama's default port - we'll expose this through Modal
OLLAMA_PORT = 11434

# Volumes
shared_volume = modal.Volume.from_name("Storage", create_if_missing=True)


# ----------------------------------------
# Image Definitions
# ----------------------------------------

# Classifier
classifierImage = (
    modal.Image.debian_slim()
    .apt_install("gcc", "curl")
    .add_local_dir("src", "/app/src")
    .add_local_dir("data", "/app/data")
    .add_local_dir("bin", "/app/bin")
    .run_commands(
        [
            "echo 'Giving execute permissions to the script...'",
            "chmod +x /app/src/run.sh",
            "echo 'Compiling binaries...'",
            "gcc /app/bin/lexer.c -o /app/src/lexer",
            "gcc /app/bin/parser.c -o /app/src/parser",
            "echo 'Image ready!'"
        ]
    )
    .env({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"})
)

## Ollama
ollama_model_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("curl", "ca-certificates")
    .pip_install(
        "fastapi==0.115.8",
        "uvicorn[standard]==0.34.0",
        "openai~=1.30",  # Pin OpenAI version for compatibility
    )
    .run_commands(
        "echo 'Installing Ollama...'",
        f"OLLAMA_VERSION={OLLAMA_VERSION} curl -fsSL https://ollama.com/install.sh | sh",
        "echo 'Ollama installed at $(which ollama)'",
        f"mkdir -p {MODEL_DIR}",
    )
    .env(
        {
            # Configure Ollama to serve on its default port
            "OLLAMA_HOST": f"0.0.0.0:{OLLAMA_PORT}",
            "OLLAMA_MODELS": MODEL_DIR,  # Tell Ollama where to store models
        }
    )
)


## Evaluation Image
evaluation_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("gcc", "g++", "java")
    .pip_install("wandb")
    .add_local_dir("src", "/app/src")
)


# ----------------------------------------
# Classifier Service
# ----------------------------------------

@app.cls(
    image=classifierImage,
    volumes={CLASSIFIER_DIR: shared_volume},  # Mount our classifier storage
    timeout=60 * 5,  # 5 minutes max input runtime
    gpu="none"
)

class Classifier:
    process: subprocess.Popen | None = None

    @modal.enter()
    def start(self):
        print("Launching Classifier...")
        self.process = subprocess.Popen(
            ["/app/src/run.sh"], shell=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    

    @modal.exit()
    def stop(self):
        if self.process:
            self.process.terminate()
            print("Classifier terminated.")


# ----------------------------------------
# Ollama Service
# ----------------------------------------
@app.cls(
    image=ollama_model_image,
    volumes={MODEL_DIR: shared_volume},
    gpu="H100",
    timeout=60 * 10,
    min_containers=1,
)

class OllamaService:
    process: subprocess.Popen | None = None

    @modal.enter()
    async def start_ollama(self):
        """Starts the Ollama server and ensures required models are downloaded."""
        print("Starting Ollama setup...")

        print(f"Starting Ollama server on port {OLLAMA_PORT}...")
        cmd = ["ollama", "serve"]
        self.ollama_process = subprocess.Popen(cmd)
        print(f"Ollama server started with PID: {self.ollama_process.pid}")

        # Wait for server to initialize
        await asyncio.sleep(10)
        print("Ollama server should be ready.")

        # --- Model Management ---
        # Check which models are already downloaded, and pull any that are missing
        loop = asyncio.get_running_loop()
        models_pulled = False  # Track if we pulled any model

        # Get list of currently available models
        ollama_list_proc = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True
        )

        if ollama_list_proc.returncode != 0:
            print(f"Error: 'ollama list' failed: {ollama_list_proc.stderr}")
            raise RuntimeError(
                f"Failed to list Ollama models: {ollama_list_proc.stderr}"
            )

        current_models_output = ollama_list_proc.stdout
        print("Current models detected:", current_models_output)

        # Download each requested model if not already present
        for model_name in MODELS_TO_DOWNLOAD:
            print(f"Checking for model: {model_name}")
            model_tag_to_check = (
                model_name if ":" in model_name else f"{model_name}:latest"
            )

            if model_tag_to_check not in current_models_output:
                print(
                    f"Model '{model_name}' not found. Pulling (output will stream directly)..."
                )
                models_pulled = True  # Mark that a pull is happening

                # Pull the model - this can take a while for large models
                pull_process = await asyncio.create_subprocess_exec(
                    "ollama",
                    "pull",
                    model_name,
                )

                # Wait for the pull process to complete
                retcode = await pull_process.wait()

                if retcode != 0:
                    print(f"Error pulling model '{model_name}': exit code {retcode}")
                else:
                    print(f"Model '{model_name}' pulled successfully.")
            else:
                print(f"Model '{model_name}' already exists.")

            # Commit the volume only if we actually pulled new models
            if models_pulled:
                print("Committing model volume...")
                await loop.run_in_executor(None, shared_volume.commit)
                print("Volume commit finished.")

        print("Ollama setup complete.")

    @modal.exit()
    def stop_ollama(self):
        """Terminates the Ollama server process on shutdown."""
        print("Shutting down Ollama server...")
        if self.ollama_process and self.ollama_process.poll() is None:
            print(f"Terminating Ollama server (PID: {self.ollama_process.pid})...")
            try:
                self.ollama_process.terminate()
                self.ollama_process.wait(timeout=10)
                print("Ollama server terminated.")
            except subprocess.TimeoutExpired:
                print("Ollama server kill required.")
                self.ollama_process.kill()
                self.ollama_process.wait()
            except Exception as e:
                print(f"Error shutting down Ollama server: {e}")
        else:
            print("Ollama server process already exited or not found.")
        print("Shutdown complete.")

    @modal.web_server(port=OLLAMA_PORT, startup_timeout=180)
    def serve(self):
        """
        Exposes the Ollama server's API endpoints through Modal's web_server.

        This is the key function that makes Ollama's API accessible over the internet.
        The web_server decorator maps Modal's HTTPS endpoint to Ollama's internal port.
        """
        print(f"Serving Ollama API on port {OLLAMA_PORT}")

    @modal.method()
    async def run_tests(self):
        import openai
        from openai.types.chat import ChatCompletionMessageParam

        """
        Tests the Ollama server by sending various prompts to each configured model.
        Returns a dictionary of results organized by model.
        """
        print("Running tests inside OllamaServer container...")
        all_results = {}  # Store results per model

        # Configure OpenAI client to use our Ollama server
        base_api_url = f"http://localhost:{OLLAMA_PORT}/v1"
        print(f"Configuring OpenAI client for: {base_api_url}")
        client = openai.AsyncOpenAI(
            base_url=base_api_url,
            api_key="not-needed",  # Ollama doesn't require API keys
        )

        # Define some test prompts
        test_prompts = [
            "Explain the theory of relativity in simple terms.",
            "Write a short poem about a cat watching rain.",
            "What are the main benefits of using Python?",
        ]

        # Test each model with each prompt
        for model_name in MODELS_TO_TEST:
            print(f"\n===== Testing Model: {model_name} =====")
            model_results = []
            all_results[model_name] = model_results

            for prompt in test_prompts:
                print(f"\n--- Testing Prompt ---\n{prompt}\n----------------------")

                # Create message in OpenAI format
                messages: List[ChatCompletionMessageParam] = [
                    {"role": "user", "content": prompt}
                ]

                try:
                    # Call the Ollama API through the OpenAI client
                    response = await client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        stream=False,
                    )
                    assistant_message = response.choices[0].message.content
                    print(f"Assistant Response:\n{assistant_message}")
                    model_results.append(
                        {
                            "prompt": prompt,
                            "status": "success",
                            "response": assistant_message,
                        }
                    )
                except Exception as e:
                    print(
                        f"Error during API call for model '{model_name}', prompt '{prompt}': {e}"
                    )
                    model_results.append(
                        {"prompt": prompt, "status": "error", "error": str(e)}
                    )

        print("Internal tests finished.")
        return all_results
    
# ----------------------------------------
# Evaluation Service
# ----------------------------------------

@app.cls(
    image=evaluation_image,
    volumes={BENCHMARK_DIR: shared_volume},
    timeout=60 * 10,
    gpu="none",
)
class EvaluationService:
    @modal.web_server()
    async def serve(self):
        """
        Exposes the evaluation service's API endpoints through Modal's web_server.
        """
        print("Serving Evaluation API")

    @modal.method()
    async def run_evaluation(self):
        """
        Runs the evaluation process using the classifier and the models.
        This method will be called to start the evaluation.
        """
        print("Running evaluation...")

        # 

        # Save results to shared storage
        with open(f"{BENCHMARK_DIR}/results.json", "w") as f:
            json.dump(results, f)

        print("Evaluation complete.")
        return results
    