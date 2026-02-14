# 🦜🔗 LangChain Hello World (with Google Gemini)

A step-by-step learning project to get started with **LangChain** — a Python framework for building apps powered by Large Language Models (LLMs). Uses **Google Gemini** (free API).

## What Does This Project Do?

This project contains **5 beginner-friendly Python scripts**, each building on the previous one, that teach you the core concepts of LangChain:

### 1. `01_hello_langchain.py` — Basic LLM Call
- Connects to Google's Gemini model using LangChain's `ChatGoogleGenerativeAI` wrapper
- Sends a simple message ("Say hello and explain what LangChain is")
- Prints the AI response along with metadata
- **You'll learn:** How to invoke an LLM and read the response object

### 2. `02_prompt_templates.py` — Reusable Prompt Templates
- Creates a parameterized prompt with placeholders like `{audience}`, `{topic}`, `{num_sentences}`
- Uses **LCEL** (LangChain Expression Language) to pipe a prompt into an LLM: `chain = prompt | llm`
- Runs the same chain twice with different inputs (explains the internet to a 5-year-old vs. a senior engineer)
- **You'll learn:** How to build reusable, dynamic prompts instead of hardcoding them

### 3. `03_output_parsers.py` — Structured Output
- Uses `StrOutputParser` to get plain text from the LLM (instead of a full message object)
- Uses `JsonOutputParser` to get structured JSON output (a Python dict with keys like `animal` and `facts`)
- Shows a full chain: `prompt | llm | parser`
- **You'll learn:** How to parse LLM responses into usable Python data types

### 4. `04_chains_and_memory.py` — Chatbot with Memory
- Builds a multi-turn chatbot that **remembers previous messages**
- Uses `MessagesPlaceholder` to inject conversation history into the prompt
- Demonstrates context retention (remembers your name, remembers previous answers)
- **You'll learn:** How to manage conversation state for chat applications

### 5. `05_simple_rag.py` — Retrieval-Augmented Generation (RAG)
- Loads sample documents (text about LangChain, RAG, and vector databases)
- Splits them into smaller chunks using `RecursiveCharacterTextSplitter`
- Creates vector embeddings and stores them in a **FAISS** vector store
- Retrieves relevant chunks for a question, then passes them as context to the LLM
- Tests with questions that are and aren't in the knowledge base
- **You'll learn:** How to make an LLM answer questions from your own data (the core of RAG)

## Setup

```bash
# 1. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Google API key (free!)
#    Get one at: https://aistudio.google.com/app/apikey
copy .env.example .env
# Edit .env and paste your real GOOGLE_API_KEY
```

## Run

```bash
python 01_hello_langchain.py
python 02_prompt_templates.py
python 03_output_parsers.py
python 04_chains_and_memory.py
python 05_simple_rag.py
```

## Requirements

- Python 3.10+
- A free [Google API key](https://aistudio.google.com/app/apikey)