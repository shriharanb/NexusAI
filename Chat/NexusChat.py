import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from rag.RagEngine import retrieve
from LLM.model import generate_answer
def NexusAI(user_query: str) -> str:
    question = user_query
    q_lower = question.lower()

    if "your name" in q_lower or "who are you" in q_lower or "your master" in q_lower or "who is your master" in q_lower:
        response = "My name is NexusAI, and my master is SHRI HARAN B."

    else:
      result = retrieve(question)
      context = result["context"]

      if context.strip():#"After stripping spaces/newlines, if the resulting string is empty, the condition is false."
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
     # Generate response and trim trailing prompt generation
    response = generate_answer(prompt).split("###")[0].strip()
    return response
