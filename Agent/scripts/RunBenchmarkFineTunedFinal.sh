#!/bin/bash

# Start time
START_TIME=$(date +%s)

# Agent configuration
#MODEL_NAME="hf.co/GhostMopey115/gemma-finetune-gguf"
#MODEL_NAME="hf.co/GhostMopey115/gemma-finetuned-transformers-gguf"
#MODEL_NAME="gemma3:27b"
MODEL_NAME="hf.co/GhostMopey115/model_16_final"
T=0.35
P=1
C=0.00
CONFIG_FILE="config/basic.yaml"

# K-Testing configuration
K=3
TIME=$(date +%Y-%m-%d_%H-%M-%S)

# Path references
ROOT_DIR=$(cd ../.. && pwd)
TRAJECTORY_DIR="$ROOT_DIR/Benchmark/runs/${MODEL_NAME}__t-${T}__p-${P}__c-${C}___benchmark"

# Repository configuration
TESTS_REPO_URL="https://github.com/Talent-Pentagon/Tests"

# Ruta del Benchmark.json
#BENCHMARK_FILE="problems.json"
#BENCHMARK_PATH="$ROOT_DIR/Benchmark/Tests/$BENCHMARK_FILE"

BENCHMARK_FILE="fineTunedTemplateFinal.json"
BENCHMARK_PATH="$ROOT_DIR/Agent/scripts/$BENCHMARK_FILE"

# Function to clean binary patches
clean_patch() {
    local input="$1"
    local output="${2:-/tmp/clean_patch.patch}"
    if [ ! -f "$input" ]; then
        echo "❌ Archivo no encontrado: $input"
        return 1
    fi
    awk '
    BEGIN { skip = 0 }
    /^diff --git / {
        if (skip) {
            skip = 0
        }
        buffer = $0
        next
    }
    /^new file mode / {
        buffer = buffer "\n" $0
        next
    }
    /^index / {
        buffer = buffer "\n" $0
        next
    }
    /^Binary files / {
        skip = 1
        buffer = ""
        next
    }
    {
        if (skip == 0) {
            if (buffer != "") {
                print buffer
                buffer = ""
            }
            print
        }
    }
    ' "$input" > "$output"
    echo "✅ Patch limpio guardado en: $output"
}

cd "$ROOT_DIR/Benchmark"

# Clone or update Tests
if [ ! -d "Tests" ]; then
    git clone "$TESTS_REPO_URL"
else
    echo "Repository already exists. Cleaning up..."
    rm -rf Tests
    git clone "$TESTS_REPO_URL"
fi

# Ensure Benchmark.json exists
echo "Using Benchmark file: $BENCHMARK_PATH"
if [ ! -f "$BENCHMARK_PATH" ]; then
    echo "❌ Benchmark Template not found at: $BENCHMARK_PATH"
    exit 1
fi

# Prepare Benchmark folder and clone repo
if [ ! -d "$ROOT_DIR/Benchmark" ]; then
    mkdir "$ROOT_DIR/Benchmark"
fi

# Output file
OUTPUT_FILE="$ROOT_DIR/Benchmark/resultsFinetunedFinal.json"
echo '{' > "$OUTPUT_FILE"
echo '\"tests\": [' >> "$OUTPUT_FILE"

index=0
jq -c '.[]' "$BENCHMARK_PATH" | while read -r item; do
    test_module=$(echo "$item" | jq -r '.test_module')
    language=$(echo "$item" | jq -r '.language' | sed 's/c++/cpp/')
    category=$(echo "$item" | jq -r '.category')
    description=$(echo "$item" | jq -r '.description')
    filename=$(echo "$item" | jq -r '.filename')

    if [[ -z "$test_module" || -z "$language" || -z "$filename" ]]; then
        echo "❌ Missing fields in JSON entry: $item"
        continue
    fi

    if [[ "$language" != "c" && "$language" != "cpp" && "$language" != "java" ]]; then
        echo "❌ Unsupported language: $language"
        continue
    fi

    responses=()
    for ((i=1; i<=K; i++)); do
        cd "$ROOT_DIR/Agent/src"
        ISSUE_DIR="../../Benchmark/Tests/$language/test$test_module.md"
        TEST_REPO_DIR="../../Benchmark/Tests"

        # Execute sweagent with 5-minute timeout
        if ! gtimeout 600s sweagent run \
          --config=$CONFIG_FILE \
          --problem_statement.path=$ISSUE_DIR \
          --env.repo.path=$TEST_REPO_DIR \
          --agent.model.temperature=$T \
          --agent.model.top_p=$P \
          --output_dir=$TRAJECTORY_DIR \
          --problem_statement.id="benchmark_run_finetuned_final" \
          --agent.model.name="ollama/$MODEL_NAME"; then
          
          echo "❌ Timeout exceeded for $test_module (run $i)"
          responses+=("\"❌ Timeout exceeded for run $i\"")
          continue
      fi

        cd "$ROOT_DIR/Benchmark/Tests/"
        PATCH="$TRAJECTORY_DIR/benchmark_run_finetuned_final/benchmark_run_finetuned_final.patch"
        CLEAN_PATCH="/tmp/clean_benchmark_run.patch"

        # Clean last artifact
        rm -f "$CLEAN_PATCH"
        clean_patch "$PATCH" "$CLEAN_PATCH"

        git apply "$CLEAN_PATCH"
        if [ $? -ne 0 ]; then
            echo "❌ Failed to apply patch for $test_module (run $i)"
            responses+=("\"❌ Patch failed for run $i\"")
            continue
        fi

        PATCHED_FILE="$ROOT_DIR/Benchmark/Tests/$language/$filename"
        if [ -f "$PATCHED_FILE" ]; then
            full_code=$(<"$PATCHED_FILE")
            escaped_code=$(jq -Rn --arg code "$full_code" '$code')
            
            # Path to .traj file
            TRAJ_FILE="$TRAJECTORY_DIR/benchmark_run_finetuned_final/benchmark_run_finetuned_final.traj"
            if [ -f "$TRAJ_FILE" ]; then
                # Extract model_stats as JSON
                model_stats=$(jq '.info.model_stats' "$TRAJ_FILE")
            else
                model_stats="{}"
            fi
            
            # Combine code and stats into a single object
            combined=$(jq -n \
                --argjson code "$escaped_code" \
                --argjson stats "$model_stats" \
                '{code: $code, model_stats: $stats}')
            
            responses+=("$combined")
        else
            echo "❌ File not found: $PATCHED_FILE (run $i)"
            responses+=("\"❌ Patched file not found: $PATCHED_FILE\"")
        fi

        git reset --hard HEAD
        git clean -fd
    done

    response_array=$(printf ",%s" "${responses[@]}")
    response_array="[${response_array:1}]"

    result=$(jq -n \
        --arg test_module "$test_module" \
        --arg language "$language" \
        --arg category "$category" \
        --arg description "$description" \
        --arg filename "$filename" \
        --argjson code "$response_array" \
        '{test_module: $test_module, language: $language, category: $category, description: $description, filename: $filename, code: $code}')

    # Add comma if not the first result
    if [ $index -ne 0 ]; then
        echo "," >> "$OUTPUT_FILE"
    fi
    echo "$result" >> "$OUTPUT_FILE"
    index=$((index + 1))
done

# Time Tracking
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_FMT=$(printf "%02d:%02d:%02d" $((DURATION/3600)) $((DURATION%3600/60)) $((DURATION%60)))

# Close tests array
echo "]," >> "$OUTPUT_FILE"

jq -n \
    --arg model "$MODEL_NAME" \
    --argjson temperature "$T" \
    --argjson top_p "$P" \
    --argjson coherence "$C" \
    --argjson k "$K" \
    --arg duration "$DURATION_FMT" \
    '{model: $model, temperature: $temperature, top_p: $top_p, coherence: $coherence, k: $k, time_elapsed: $duration}' | sed 's/^{//;' >> "$OUTPUT_FILE"

jq '.' $OUTPUT_FILE > tmp.json && mv tmp.json $OUTPUT_FILE
echo "✅ Results saved to: $OUTPUT_FILE"