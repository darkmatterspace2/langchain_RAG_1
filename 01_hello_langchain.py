"""
01 - Hello LangChain! 🚀
========================
The simplest possible LangChain program.
We invoke an LLM with a plain string prompt and print the response.

Concepts covered:
  - ChatGoogleGenerativeAI (the LLM wrapper for Gemini)
  - HumanMessage
  - Invoking the model
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file (GOOGLE_API_KEY)
load_dotenv()

# 1. Create an LLM instance
#    - model: which Gemini model to use
#    - temperature: 0 = deterministic, 1 = creative
llm = ChatGoogleGenerativeAI(model="gemma-3-1b-it", temperature=0.7)

# 2. Send a message and get a response
response = llm.invoke([HumanMessage(content="Say hello and explain what LangChain is in 2 sentences.")])

# 3. Print the result
print("=" * 60)
print("🤖 LLM Response:")
print("=" * 60)
print(response.content)
print("=" * 60)
print(f"\n📊 Metadata: {response.response_metadata}")
