import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from rag.RagEngine import retrieve
from LLM.model import generate_answer

def NexusAI(user_query: str) -> str:
    question = user_query
    q_lower = question.lower().strip()

    # 1. Check for direct identity/persona overrides first
    if "your name" in q_lower or "who are you" in q_lower or "your master" in q_lower or "who is your master" in q_lower:
        return "My name is NexusAI, and my master is SHRI HARAN B."

    # 🌟 2. Handle basic friendly greetings instantly for responsive feedback
    elif q_lower in ["hi", "hii", "hello", "hey", "good afternoon", "good morning", "good evening"]:
        return "Hii Master! How can I assist you today?"

    # 3. Otherwise, fall back to RAG retrieval pipeline blocks safely
    else:
        result = retrieve(question)
        context = result.get("context", "")

        if context.strip():
            prompt = f"""
### SYSTEM PERSONA
Your name is NexusAI. Your master is SHRI HARAN B.

### INSTRUCTIONS
Answer the user's question directly based on the data below. Do not mention the words "context" or "document".

### PROVIDED DATA
{context}

### USER QUESTION
{question}

### DIRECT ANSWER
"""
        else:
            prompt = f"""
### SYSTEM PERSONA
Your name is NexusAI. Your master is SHRI HARAN B.

### INSTRUCTIONS
Answer the question using your own internal knowledge.

### USER QUESTION
{question}

### DIRECT ANSWER
"""
        
        # This execution lane only triggers when the RAG prompt variables have been safely built
        response = generate_answer(prompt).split("###")[0].strip()
        return response