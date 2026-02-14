"""
08 - Groq Inference ⚡
======================
Use Groq's ultra-fast inference API with llama-3.3-70b-versatile.
Groq runs LLMs on custom LPU hardware — extremely fast responses.

Uses:
  - langchain-groq for the LLM
  - llama-3.3-70b-versatile model
  - Free Groq API key from https://console.groq.com/keys
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ─── Create the Groq LLM ────────────────────────────────────
# llama-3.3-70b supports system prompts!
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

# ─── Example 1: Simple call ─────────────────────────────────
print("=" * 60)
print("⚡ Groq + LLaMA 3.3 70B — Simple Call")
print("=" * 60)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Keep answers concise (2-3 sentences)."),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"question": "What is LangChain and why is it useful?"})
print(f"\n{response}\n")

# ─── Example 2: Interactive chat ─────────────────────────────
print("=" * 60)
print("💬 Interactive Chat (type 'quit' to exit)")
print("=" * 60)

while True:
    try:
        question = input("\n❓ You: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Bye!")
        break

    if not question:
        continue
    if question.lower() in ("quit", "exit", "q"):
        print("👋 Bye!")
        break

    answer = chain.invoke({"question": question})
    print(f"🤖 LLaMA: {answer}")
