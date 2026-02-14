"""
02 - Prompt Templates 📝
========================
Instead of hardcoding prompts, use PromptTemplates to create
reusable, parameterized prompts.

Concepts covered:
  - ChatPromptTemplate
  - Template variables (placeholders)
  - Formatting prompts with .invoke()
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 1. Create a prompt template with placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who explains things simply for a {audience}."),
    ("human", "Explain {topic} in {num_sentences} sentences."),
])

# 2. Create the LLM
llm = ChatGoogleGenerativeAI(model="gemma-3-27b-it", temperature=0.7)

# 3. Create a chain by piping the prompt into the LLM
chain = prompt | llm  # This is LCEL (LangChain Expression Language)!

# 4. Invoke the chain with variables
response = chain.invoke({
    "audience": "5-year-old",
    "topic": "how the internet works",
    "num_sentences": "3",
})

print("=" * 60)
print("🧒 Explanation for a 5-year-old:")
print("=" * 60)
print(response.content)

# 5. Reuse the same chain with different inputs!
response2 = chain.invoke({
    "audience": "senior software engineer",
    "topic": "how the internet works",
    "num_sentences": "3",
})

print("\n" + "=" * 60)
print("👨‍💻 Explanation for a senior engineer:")
print("=" * 60)
print(response2.content)
