FROM python:3.11

# Set the working directory
WORKDIR /app

# Install system dependencies (nodejs, npm, gcc, g++, make, java, curl)
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    gcc \
    g++ \
    make \
    openjdk-17-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI using the official Docker installation script
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh  # Clean up

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Copy the application code
COPY . /app

# Install Python dependencies
RUN pip install -e .

# Pre-install frontend (React) dependencies
RUN cd sweagent/frontend && npm install