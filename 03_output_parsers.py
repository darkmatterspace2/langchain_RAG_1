"""
03 - Output Parsers 🔧
======================
Parse the LLM's text output into structured Python objects
(like dicts/lists) instead of raw strings.

Concepts covered:
  - StrOutputParser (get plain text)
  - JsonOutputParser (get structured JSON)
  - Full LCEL chain: prompt | llm | parser
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# ─── Example 1: StrOutputParser ──────────────────────────────
# Returns just the text content (strips away message metadata)
print("=" * 60)
print("📝 Example 1: StrOutputParser")
print("=" * 60)

prompt1 = ChatPromptTemplate.from_messages([
    ("human", "Give me a fun fact about {animal}."),
])

chain1 = prompt1 | llm | StrOutputParser()
result1 = chain1.invoke({"animal": "octopus"})

print(result1)  # This is a plain string, not an AIMessage object!
print(f"Type: {type(result1)}")  # <class 'str'>


# ─── Example 2: JsonOutputParser ────────────────────────────
# Parses LLM output into a Python dict
print("\n" + "=" * 60)
print("📊 Example 2: JsonOutputParser")
print("=" * 60)

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "Always respond in valid JSON format. No markdown, no code fences, just raw JSON."),
    ("human",
     "Give me 3 fun facts about {animal}. "
     "Return as JSON with keys: 'animal' and 'facts' (a list of strings)."),
])

chain2 = prompt2 | llm | JsonOutputParser()
result2 = chain2.invoke({"animal": "dolphin"})

print(f"Type: {type(result2)}")  # <class 'dict'>
print(f"Animal: {result2['animal']}")
for i, fact in enumerate(result2["facts"], 1):
    print(f"  {i}. {fact}")
