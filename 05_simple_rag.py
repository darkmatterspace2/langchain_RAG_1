"""
05 - Simple RAG (Retrieval-Augmented Generation) 📚
===================================================
The crown jewel! Ask questions about your OWN data by:
  1. Splitting text into chunks
  2. Creating embeddings & storing in a vector store
  3. Retrieving relevant chunks for a question
  4. Passing them to the LLM as context

Concepts covered:
  - Document loading (from raw text)
  - Text splitting
  - Embeddings (Google Generative AI)
  - In-memory vector store (FAISS)
  - Retrieval chain
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ─── Step 1: Our "knowledge base" (normally you'd load files) ───
raw_documents = [
    Document(page_content="""
    LangChain is a framework for developing applications powered by large language models (LLMs).
    It was created by Harrison Chase and first released in October 2022.
    LangChain provides tools for prompt management, chains, memory, and retrieval-augmented generation.
    The framework supports Python and JavaScript/TypeScript.
    """),
    Document(page_content="""
    Retrieval-Augmented Generation (RAG) is a technique that enhances LLM responses
    by first retrieving relevant documents from a knowledge base, then passing them
    as context to the LLM. This helps reduce hallucinations and keeps responses
    grounded in factual data. RAG was introduced by Facebook AI Research in 2020.
    """),
    Document(page_content="""
    Vector databases store data as high-dimensional vectors (embeddings).
    Popular vector databases include FAISS, Pinecone, Weaviate, and Chroma.
    They enable semantic search - finding documents by meaning rather than keywords.
    FAISS (Facebook AI Similarity Search) is an open-source library for efficient
    similarity search, developed by Meta AI Research.
    """),
]

# ─── Step 2: Split documents into smaller chunks ────────────
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,       # Max characters per chunk
    chunk_overlap=50,     # Overlap between chunks for continuity
)
chunks = text_splitter.split_documents(raw_documents)
print(f"📄 Split {len(raw_documents)} documents into {len(chunks)} chunks\n")

# ─── Step 3: Create embeddings and vector store ─────────────
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
vector_store = FAISS.from_documents(chunks, embeddings)

# ─── Step 4: Create a retriever ─────────────────────────────
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},  # Return top 3 most relevant chunks
)

# ─── Step 5: Build the RAG chain ────────────────────────────
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Answer the question based ONLY on the following context. "
     "If the context doesn't contain the answer, say 'I don't have that information.'\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])


def format_docs(docs):
    """Join retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# ─── Step 6: Ask questions! ─────────────────────────────────
questions = [
    "What is LangChain and who created it?",
    "What is RAG and why is it useful?",
    "What is FAISS?",
    "What is the capital of France?",  # Not in our knowledge base!
]

print("=" * 60)
print("📚 RAG Q&A Demo")
print("=" * 60)

for q in questions:
    print(f"\n❓ Question: {q}")
    answer = rag_chain.invoke(q)
    print(f"✅ Answer:   {answer}")

print("\n" + "=" * 60)
print("🎉 Done! You've built a RAG pipeline!")
print("=" * 60)
