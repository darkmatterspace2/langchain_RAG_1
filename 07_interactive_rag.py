"""
07 - Interactive RAG Chat 💬📂
==============================
Same RAG pipeline as 06, but you type your own questions
in the terminal. Type 'quit' or 'exit' to stop.

Uses:
  - gemma-3-27b-it for the LLM
  - gemini-embedding-001 for embeddings
  - FAISS vector store
  - TextLoader for the .txt file
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
llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0)

rag_prompt = ChatPromptTemplate.from_messages([
    ("human",
     "You are a helpful assistant. Answer the question based ONLY "
     "on the context provided below. If the context does not contain the "
     "answer, say 'I don't have that information in the document.'\n\n"
     "Context:\n{context}\n\n"
     "Question: {question}"),
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
print(f"💬 Ask anything about: {os.path.basename(FILE_PATH)}")
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
