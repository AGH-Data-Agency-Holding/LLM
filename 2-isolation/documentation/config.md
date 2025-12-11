# Configuration Module

## Overview
`config.py` centralizes all configuration settings for the LLM service system. It uses environment variables with sensible defaults for local development.

## Features
- Environment variable loading via `python-dotenv`
- Centralized configuration management
- Application ID mappings
- Path management with OS compatibility

## Configuration Sections

### Service Parameters
```python
REDIS_HOST = 'localhost'  # Redis server host
REDIS_PORT = 6379         # Redis server port
REDIS_DB = 0              # Redis database number
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama endpoint

