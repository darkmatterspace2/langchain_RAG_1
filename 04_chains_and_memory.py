"""
04 - Conversation Memory 💬
===========================
Build a chatbot that remembers previous messages in the
conversation using message history.

Concepts covered:
  - ChatPromptTemplate with MessagesPlaceholder
  - Manual conversation history management
  - Multi-turn conversations
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

# 1. Create a prompt that includes a placeholder for chat history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant named Buddy. Keep responses concise (1-2 sentences)."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm

# 2. Maintain conversation history as a list of messages
chat_history = []

def chat(user_input: str) -> str:
    """Send a message and update the chat history."""
    response = chain.invoke({
        "chat_history": chat_history,
        "input": user_input,
    })

    # Add both the user message and AI response to history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response.content))

    return response.content


# 3. Have a multi-turn conversation
print("=" * 60)
print("💬 Multi-turn Conversation Demo")
print("=" * 60)

conversations = [
    "Hi! My name is Alex.",
    "What's my name?",              # Tests if it remembers!
    "What's 2 + 2?",
    "Multiply that result by 10.",   # Tests if it remembers context!
]

for msg in conversations:
    print(f"\n🧑 You:   {msg}")
    reply = chat(msg)
    print(f"🤖 Buddy: {reply}")

print("\n" + "=" * 60)
print(f"📜 Total messages in history: {len(chat_history)}")
print("=" * 60)
