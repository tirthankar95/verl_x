# Use an official Python 3.12 image as base
FROM python:3.12.3-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (adjust as needed for pyarrow, flash-attn, torch, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create working directory and mount point
WORKDIR /app

# Create mount points (optional but good practice)
RUN mkdir -p /app/models /app/rlf-small-lm-grid-puzzles
RUN echo 'Winter is coming.'
# Copy your code and requirements
COPY requirements.txt /app/requirements.txt

# Upgrade pip, install requirements
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN pip install flash-attn==2.8.0.post2 --no-build-isolation
# Default shell
CMD ["/bin/sh"]

