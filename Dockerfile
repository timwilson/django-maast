# Use the specified base image
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install some system packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Copy the project files to the container
COPY . .

# Update pip and Install Poetry
RUN python -m pip install --upgrade pip && \
    pip install poetry

# Disable virtual env creation by Poetry as Docker container itself is isolated
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-dev
