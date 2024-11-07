# DBpedia Hybrid Search System

A hybrid search system that combines traditional keyword search with semantic search capabilities to query DBpedia data using Vespa.

## Overview

This project implements a search system with the following key features:

- **Data Source**: Uses DBpedia data containing articles with titles and text content
- **Search Capabilities**: 
  - Keyword-based search using BM25 ranking
  - Semantic search using embeddings
  - Hybrid search combining both approaches
- **Technology Stack**:
  - Vespa for search and ranking
  - Python for data processing and search interface
  - Hugging Face transformers for text embeddings (Snowflake Arctic model)

## System Components

### 1. Data Pipeline
- `dbpedia_data.py`: Fetches data from DBpedia using SPARQL queries
- `process_data_to_jsonl.py`: Processes the raw data into JSONL format for Vespa ingestion

### 2. Search Implementation
- `pyvespa_search.py`: Implements search functionality using PyVespa including:
  - Keyword search
  - Semantic search
  - Embedding-based similarity search

### 3. Vespa Configuration
- `services.xml`: Defines the Vespa service configuration including:
  - Document processing
  - Embedding model configuration (Snowflake Arctic)
  - Search endpoints
- `schemas/doc.sd`: Defines the document schema with:
  - Text fields (title, text) with BM25 indexing
  - Embedding field for semantic search
  - Multiple ranking profiles

## Key Features

1. **Hybrid Search**:
   - Combines traditional keyword search with semantic understanding
   - Multiple ranking profiles for different search needs

2. **Semantic Capabilities**:
   - Uses neural embeddings for semantic understanding
   - Supports similarity search based on document embeddings

3. **Flexible Architecture**:
   - Modular components for data processing and search
   - Configurable ranking profiles
   - Scalable document processing pipeline

## Learnings

1. **Search Architecture**:
   - Importance of combining multiple search approaches
   - Trade-offs between keyword and semantic search
   - Benefits of hybrid search systems

2. **Data Processing**:
   - Handling structured data from DBpedia
   - Importance of proper data cleaning and formatting
   - Managing large datasets efficiently

3. **Vespa Integration**:
   - Configuration of search services
   - Implementation of multiple ranking profiles
   - Integration of neural embeddings

4. **Performance Considerations**:
   - Balancing search accuracy and speed
   - Importance of proper indexing
   - Impact of embedding dimensions on performance

> Note: This is part of the DATA-226 Classwork
