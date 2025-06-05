FROM gcc:latest

# Set working directory inside the container
WORKDIR /app

# Copy only the source code folder
COPY src/ ./src/

# Copy data folder for testing
COPY data/ ./data/
COPY bin/ ./bin/

# Optional: Copy responses if needed
# COPY responses/ ./responses/

# Compile the C programs
RUN gcc -o ./src/lexer ./src/lexer.c
RUN gcc -o ./src/parser ./src/parser.c

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Set default command to bash (interactive)
CMD ["/bin/bash"]
