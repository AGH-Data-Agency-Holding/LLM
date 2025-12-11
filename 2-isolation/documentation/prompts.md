
## 4. README for `prompts.py`

# Prompts Module

## Overview
`prompts.py` contains application-specific prompt templates for the LLM service system. Each prompt includes strict domain boundaries and context-aware instructions.

## Structure
Each prompt follows this structure:
1. **Role Definition**: Specifies the assistant's expertise
2. **Domain Rule**: Strict instruction for out-of-domain queries
3. **Available Context**: Placeholder for RAG context
4. **User Question**: Placeholder for user query
5. **Guidelines**: Instructions for response generation

## Available Prompts

### 1. Application_Recette
**Purpose**: Cooking and recipes assistant
**Key Features**:
- Strictly limited to culinary topics
- Provides recipe-specific responses
- Rejects non-culinary queries with polite redirection

### 2. Application_Quran
**Purpose**: Quranic studies assistant
**Key Features**:
- Specialized in Quranic verses, surahs, and tafsir
- Maintains religious accuracy
- Redirects non-Quranic queries appropriately

### 3. Application_Qissas
**Purpose**: Prophets stories assistant
**Key Features**:
- Focused on stories of Prophets (Qissas al Anbiyae)
- Provides moral lessons from prophetic narratives
- Rejects queries outside prophetic stories

## Prompt Design Principles

### 1. Domain Isolation
Each prompt includes strict instructions to reject queries outside its domain. This ensures:
- Application-specific behavior
- Prevention of cross-domain contamination
- Clear user expectations

### 2. Context Integration
Prompts are designed to integrate RAG context effectively:
- Context is inserted via `{context}` placeholder
- Guidelines prioritize context usage
- Fallback to general knowledge when context is insufficient

### 3. Safety and Appropriateness
- Polite rejection for out-of-domain queries
- Clear redirection to appropriate topics
- Maintenance of professional tone

## Usage Example
```python
from prompts import PROMPTS_BY_APPLICATIONS

# Get prompt for Recipes application
recipes_prompt = PROMPTS_BY_APPLICATIONS["Application_Recette"]

# Format with context and query
formatted_prompt = recipes_prompt.format(
    context="Available recipe data...",
    query="How to make Moroccan potato salad?"
)
