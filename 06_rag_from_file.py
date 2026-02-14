"""
06 - RAG from a Text File 📂
============================
Load a real .txt file, split it, embed it, and ask questions
about its content using Retrieval-Augmented Generation.

Uses:
  - gemma-3-27b-it (supports system prompts)
  - gemini-embedding-001 for embeddings
  - FAISS for the vector store
  - TextLoader to load a .txt file

Concepts covered:
  - Loading documents from files (TextLoader)
  - End-to-end file-based RAG pipeline
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ─── Configuration ──────────────────────────────────────────
FILE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
LLM_MODEL = "gemma-3-27b-it"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# ─── Step 1: Load the document from a .txt file ─────────────
print(f"📂 Loading document: {FILE_PATH}")
loader = TextLoader(FILE_PATH, encoding="utf-8")
documents = loader.load()
print(f"   Loaded {len(documents)} document(s), "
      f"total {sum(len(d.page_content) for d in documents)} characters\n")

# ─── Step 2: Split into chunks ──────────────────────────────
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,       # Characters per chunk
    chunk_overlap=50,     # Overlap for context continuity
    separators=["\n\n", "\n", ". ", " ", ""],  # Split by paragraphs first
)
chunks = text_splitter.split_documents(documents)
print(f"✂️  Split into {len(chunks)} chunks")
for i, chunk in enumerate(chunks):
    print(f"   Chunk {i+1}: {len(chunk.page_content)} chars — \"{chunk.page_content[:60]}...\"")
print()

# ─── Step 3: Create embeddings and vector store ─────────────
print("🔢 Creating embeddings and building vector store...")
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vector_store = FAISS.from_documents(chunks, embeddings)
print("   ✅ Vector store ready!\n")

# ─── Step 4: Create the retriever ───────────────────────────
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},  # Top 3 most relevant chunks
)

# ─── Step 5: Build the RAG chain ────────────────────────────
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0)

# NOTE: Gemma models don't support system prompts via Google AI API,
# so we put the instructions directly in the human message.
rag_prompt = ChatPromptTemplate.from_messages([
    ("human",
     "You are a helpful assistant. Answer the question based ONLY "
     "on the context provided below. If the context does not contain the "
     "answer, say 'I don't have that information in the document.'\n\n"
     "Context:\n{context}\n\n"
     "Question: {question}"),
])


def format_docs(docs):
    """Join retrieved document chunks into a single string."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# ─── Step 6: Ask questions about the file! ─────────────────
questions = [
    "Who created Python?",
    "What is PIP?",
    "What features did Python 3.12 introduce?",
    "Which companies use Python?",
    "What is the capital of Japan?",  # Not in the file — tests grounding!
]

print("=" * 60)
print(f"📚 RAG Q&A — asking {LLM_MODEL} about knowledge_base.txt")
print("=" * 60)

for q in questions:
    print(f"\n❓ {q}")
    answer = rag_chain.invoke(q)
    print(f"✅ {answer}")

print("\n" + "=" * 60)
print("🎉 Done! Try replacing knowledge_base.txt with your own file!")
print("=" * 60)
