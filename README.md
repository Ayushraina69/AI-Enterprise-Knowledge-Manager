# AI Enterprise Knowledge Manager

An AI-powered enterprise knowledge management system built with multi-agent architecture, RAG, vector search, memory, and specialized knowledge agents.

## Overview

The AI Enterprise Knowledge Manager helps employees retrieve information from internal company documents using natural-language questions.

The system uses an orchestrator agent that routes each question to the most appropriate specialist agent.

## Key Features

- Multi-agent architecture
- Enterprise knowledge search
- RAG with ChromaDB
- Local sentence-transformer embeddings
- Specialized policy, document, meeting, knowledge, and project/SOP agents
- Agent handoffs
- Conversation memory
- Company document retrieval
- Error handling
- Source-aware responses
- Local vector database

## Agent Architecture

```text
User
  |
  v
Enterprise Knowledge Orchestrator
  |
  +--> Knowledge Search Agent
  |
  +--> Document Reader Agent
  |
  +--> Policy Expert Agent
  |
  +--> Meeting Intelligence Agent
  |
  +--> Project/SOP Agent