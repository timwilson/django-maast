# Use the specified base image
FROM python:3.12-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install some system packages

RUN apk add ca-certificates gcc musl-dev libffi-dev nodejs npm \
    && rm -rf /var/cache/apk/*

# Copy Python dependencies
COPY pyproject.toml poetry.lock* ./

# Update pip and Install Poetry
RUN python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

# Copy the project files to the container
COPY . .
