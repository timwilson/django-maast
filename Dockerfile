# Use the specified base image
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install some system packages
RUN apt update && apt upgrade -y && apt install -y \
    curl \
    gnupg \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | \
    gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
ARG NODE_MAJOR=20
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | \
    tee /etc/apt/sources.list.d/nodesource.list
RUN apt update && apt install -y nodejs

# Set working directory
WORKDIR /code

# Update pip and Install Poetry
RUN python -m pip install --upgrade pip && \
    pip install poetry

# Disable virtual env creation by Poetry as Docker container itself is isolated
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install

# Copy the project files to the container
COPY . .
