# 🎓 MCP-Based AI Learning Coach

> An intelligent, adaptive learning platform powered by **MCP (Model Context Protocol)**, **RAG**, and **Agentic AI** — built to personalize education for every learner.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [MCP Tools](#mcp-tools)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Dataset](#dataset)
- [Features](#features)
- [Real-World Example](#real-world-example)
- [Why This Project is Advanced](#why-this-project-is-advanced)

---

## Overview

Traditional learning systems give every student the same content, fixed difficulty, and zero personalization. This project solves that by combining:

- **MCP (Model Context Protocol)** — to orchestrate multiple intelligent AI tools
- **RAG (Retrieval-Augmented Generation)** — for context-aware, accurate answers from the knowledge base
- **Agentic AI Workflow** — to dynamically guide learners like a personal AI tutor

The result is a system that **understands** each learner, **adapts** content in real time, and **explains** concepts clearly — all fully AI-powered.

---

## Architecture

```
User
 |
 v
[Frontend — React + Tailwind CSS]
  Dashboard | Learning Page | Chatbot | Leaderboard
 |
 | HTTP / REST
 v
[Backend — FastAPI]
  API Routing | Auth | LLM Communication
 |
 v
[MCP Orchestrator]
  Context Manager | Tool Selector | Decision Flow
 |
 +------------------+------------------+------------------+
 |                  |                  |                  |
 v                  v                  v                  v
[Knowledge      [Learner         [Adaptive         [Question
 Graph Tool]     Profiling Tool]  Difficulty Tool]  Generator Tool]

 +------------------+------------------+------------------+
 |                  |                  |
 v                  v                  v
[Explanation    [Vector Memory    [Progress
 Generator]      Tool — RAG]       Analytics Tool]
 |                  |
 v                  v
[LLM Engine]    [Vector Store]
 OpenAI /        FAISS / Chroma
 Anthropic /
 Gemini
 |
 v
[Dataset — questions.csv]
 ML | Deep Learning | NLP | GenAI | Engineering
```

---

## MCP Tools

The system uses **7 specialized MCP tools**, each responsible for a distinct part of the learning pipeline:

| # | Tool | Role |
|---|------|------|
| 1 | **Knowledge Graph Tool** | Stores topic relationships for structured learning paths (e.g. ML → Supervised → Regression) |
| 2 | **Learner Profiling Tool** | Tracks per-user accuracy, weak topics, and progress for full personalization |
| 3 | **Adaptive Difficulty Tool** | Raises or lowers question difficulty dynamically based on performance |
| 4 | **Question Generator Tool** | Generates questions from `questions.csv` across ML, DL, NLP, and GenAI domains |
| 5 | **Explanation Generator Tool** | Uses the LLM to produce step-by-step, concept-clear explanations |
| 6 | **Vector Memory Tool (RAG)** | Stores embeddings and retrieves relevant context for accurate, context-aware answers |
| 7 | **Progress Analytics Tool** | Tracks mastery, engagement, and performance; powers the analytics dashboard |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, Tailwind CSS |
| Backend | FastAPI (Python) |
| AI Orchestration | MCP (Model Context Protocol) |
| LLM | OpenAI / Anthropic / Gemini (configured via `.env`) |
| Vector Store | FAISS or Chroma |
| Dataset | CSV — AI & Engineering questions |

---

## Project Structure

```
learning-coach-mcp/
|
|-- learning-coach/                  (Main application)
|   |
|   |-- backend/                     (FastAPI server)
|   |   |-- main.py                  (App entry point)
|   |   |-- requirements.txt
|   |   |
|   |   |-- mcp/
|   |   |   |-- orchestrator.py      (MCP tool selector and context manager)
|   |   |   |-- tools/
|   |   |       |-- knowledge_graph.py
|   |   |       |-- learner_profiling.py
|   |   |       |-- adaptive_difficulty.py
|   |   |       |-- question_generator.py
|   |   |       |-- explanation_generator.py
|   |   |       |-- vector_memory.py
|   |   |       |-- progress_analytics.py
|   |   |
|   |   |-- rag/
|   |   |   |-- embeddings.py        (Embedding pipeline)
|   |   |   |-- retriever.py         (Vector retrieval)
|   |   |
|   |   |-- llm/
|   |       |-- client.py            (LLM API client)
|   |
|   |-- frontend/                    (React + Tailwind UI)
|   |   |-- src/
|   |   |   |-- pages/               (Dashboard, Learn, Leaderboard, Chat)
|   |   |   |-- components/          (Shared UI components)
|   |   |-- package.json
|   |
|   |-- data/
|       |-- questions.csv            (Generated question bank)
|
|-- generate_questions.py            (Script to generate questions.csv)
|-- .gitignore
|-- README.md
```

---

## How to Run

### Prerequisites

Make sure you have the following installed:

- Python **3.10+**
- Node.js **18+** and npm
- An LLM API key — OpenAI, Anthropic, or Google Gemini

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/AgalyaThanigasalam/learning-coach-mcp.git
cd learning-coach-mcp
```

---

### Step 2 — Generate the question dataset

Run this **once** from the root of the repo to create `learning-coach/data/questions.csv`:

```bash
python generate_questions.py
```

> This generates 140+ questions across ML, Deep Learning, NLP, and GenAI with 5 difficulty levels each.

---

### Step 3 — Set up the Backend

```bash
cd learning-coach/backend

# Create a virtual environment
python -m venv venv

# Activate it — macOS / Linux:
source venv/bin/activate

# Activate it — Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Open `.env` and add your LLM API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
# or
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# or
GOOGLE_API_KEY=your_gemini_api_key_here
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

- API running at: **http://localhost:8000**
- Interactive docs at: **http://localhost:8000/docs**

---

### Step 4 — Set up the Frontend

Open a **new terminal** tab/window:

```bash
cd learning-coach/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

App running at: **http://localhost:5173**

---

### Step 5 — Open in browser

Go to **http://localhost:5173** to use the Learning Coach.

> Make sure **both** the backend (port 8000) and frontend (port 5173) are running at the same time.

---

### Quick Start Summary

```bash
# Terminal 0 — Generate dataset (only once)
python generate_questions.py

# Terminal 1 — Backend
cd learning-coach/backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Add your LLM API key inside .env
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd learning-coach/frontend
npm install
npm run dev
```

---

## Dataset

The `questions.csv` is auto-generated by `generate_questions.py` and covers **5 difficulty levels** across:

| Domain | Sample Topics |
|--------|--------------|
| Machine Learning | Supervised, Unsupervised, Ensemble, Regularization, Bias-Variance |
| Deep Learning | CNNs, RNNs, LSTMs, Transformers, GANs, Diffusion models |
| NLP | Tokenization, Embeddings, Attention, Language models |
| Generative AI | Prompt engineering, LLMs, Fine-tuning, RAG |
| Engineering | Data Structures, Algorithms, System Design |

Each row contains: `domain`, `difficulty (1–5)`, `question`, `4 answer options`, `correct answer`, `explanation`.

---

## Features

- 🎯 **Personalized learning** — adapts to each student's strengths and weaknesses
- 📐 **Adaptive difficulty** — questions scale automatically with real-time performance
- 🤖 **AI explanations** — step-by-step concept clarity powered by LLMs
- 💬 **Chatbot assistant** — ask doubts and get guided explanations via MCP + LLM
- 🏆 **Leaderboard** — engagement-driven ranking across users
- 📊 **Progress analytics** — mastery and engagement tracking dashboard
- 🔍 **RAG-powered answers** — retrieval-augmented context for higher accuracy

---

## Real-World Example

> If a user struggles with **Neural Networks**:

1. **Profiling Tool** detects the weak topic from performance history
2. **Adaptive Difficulty Tool** reduces question difficulty automatically
3. **Question Generator** creates targeted Neural Network practice questions
4. **Explanation Generator** breaks down each answer step-by-step using the LLM
5. **Analytics Tool** tracks improvement and updates the progress dashboard

---

## Why This Project is Advanced

| Concept | Implementation |
|---------|---------------|
| **MCP** | Core orchestration — connects and controls all AI tools |
| **RAG** | Vector memory for context-aware, grounded responses |
| **Agentic AI** | Multi-tool decision flow — not a single chatbot |
| **Full-Stack** | React frontend + FastAPI backend |
| **Personalization** | Per-user profiling, adaptive questions, analytics |

This is **not** a static quiz app or a basic chatbot. It is a full agentic AI system that dynamically decides which tools to invoke, in what order, based on each learner's live context — combining MCP + RAG + LLM into one cohesive platform.

---

> by [Agalya Thanigasalam](https://github.com/AgalyaThanigasalam)
