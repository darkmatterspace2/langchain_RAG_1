"""
09 - Interactive RAG with Groq ⚡📂
====================================
RAG pipeline that loads knowledge_base.txt and lets you ask
questions interactively — powered by Groq + LLaMA 3.3 70B.

Uses:
  - llama-3.3-70b-versatile via Groq (supports system prompts)
  - gemini-embedding-001 for embeddings (Google)
  - FAISS vector store
  - TextLoader for the .txt file
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ─── Configuration ──────────────────────────────────────────
FILE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# ─── Step 1: Load and split the document ────────────────────
print(f"\n📂 Loading: {os.path.basename(FILE_PATH)}")
loader = TextLoader(FILE_PATH, encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
)
chunks = text_splitter.split_documents(documents)
print(f"✂️  Split into {len(chunks)} chunks")

# ─── Step 2: Build the vector store ─────────────────────────
print("🔢 Building vector store...")
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
print("✅ Ready!\n")

# ─── Step 3: Build the RAG chain ────────────────────────────
llm = ChatGroq(model=LLM_MODEL, temperature=0)

# LLaMA 3.3 supports system prompts!
rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. Answer the question based ONLY "
     "on the context provided below. If the context does not contain the "
     "answer, say 'I don't have that information in the document.'\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])


def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# ─── Step 4: Interactive Q&A loop ───────────────────────────
print("=" * 60)
print(f"⚡ Groq RAG — {LLM_MODEL}")
print(f"📄 Document: {os.path.basename(FILE_PATH)}")
print("   Type 'quit' or 'exit' to stop")
print("=" * 60)

while True:
    try:
        question = input("\n❓ Your question: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Bye!")
        break

    if not question:
        continue
    if question.lower() in ("quit", "exit", "q"):
        print("👋 Bye!")
        break

    answer = rag_chain.invoke(question)
    print(f"✅ {answer}")
