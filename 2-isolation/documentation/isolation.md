
## 2. README for `isolation.ipynb`

# Isolation Test Notebook

## Overview
This Jupyter notebook (`isolation.ipynb`) demonstrates the isolation testing of the LLM service system. It tests how different applications handle queries within and outside their domains using the smart caching system.

## Purpose
- Test application-specific behavior
- Demonstrate cache efficiency
- Measure response times
- Verify domain isolation

## Test Scenarios

### 1. Application: Qissas Anbia (Prophets Stories)
**ID:** 1234567892
- Tests queries about Prophet Muhammad
- Tests out-of-domain queries (food recipes)
- Demonstrates cache hit after first query

### 2. Application: Recipes
**ID:** 1234567890
- Tests recipes (Moroccan potato dish)
- Tests out-of-domain queries (Prophet stories)
- Shows application-specific response constraints

## Key Observations

### Cache Performance
- First query: ~9 seconds (uncached)
- Same query later: ~0.14 seconds (cached)
- 64x speed improvement with cache

### Domain Isolation
- Qissas application correctly rejects food-related queries
- Recipes application correctly rejects Prophet story queries
- Each application maintains strict domain boundaries

### Response Quality
- In-domain: Detailed, contextual responses
- Out-of-domain: Polite refusal with redirection

## Cells Breakdown

### Cell 1: Imports
- Imports `ask_llm_with_redis_smart` and `load_application_data`
- Imports `time` for performance measurement

### Cells 2-5: Qissas Application Tests
- Loads Qissas application data
- Tests Prophet Muhammad query (uncached → cached)
- Tests food query (rejected)

### Cells 6-9: Recipes Application Tests
- Loads Recipes application data
- Tests Prophet query (rejected)
- Tests Moroccan potato recipe
- Demonstrates cache for repeated queries

## Usage
Run cells sequentially to:
1. Test different applications
2. Observe cache behavior
3. Verify domain isolation
4. Measure performance improvements

## Requirements
- Running Redis server
- Ollama server (or Gemini API key)
- Pre-computed embeddings for each application
- Python dependencies from `server_utils.py`

