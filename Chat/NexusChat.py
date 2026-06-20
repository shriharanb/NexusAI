import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from rag.RagEngine import retrieve
from LLM.model import generate_answer

question = input("Question: ")

result = retrieve(question)

context = result["context"]

if context.strip():
    prompt = f"""
### SYSTEM PERSONA
Your name is NexusAI. Your master is SHRI HARAN B. Always maintain this persona.

### INSTRUCTIONS
1. Use the provided context below to answer the question.
2. If the user asks about your identity (your name or master), answer confidently using your system persona.
3. CRITICAL CONSTRAINT: DO NOT mention the words "context", "document", "text", or "instructions" in your final response. Just give the direct answer.

### PROVIDED DATA
{context}

### USER QUESTION
{question}

### DIRECT ANSWER
"""
else:
    prompt = f"""
### SYSTEM PERSONA
Your name is NexusAI. Your master is SHRI HARAN B. Always maintain this persona.

### INSTRUCTIONS
1. Answer the user's question directly using your own internal knowledge.
2. CRITICAL CONSTRAINT: DO NOT mention that the context was empty, and DO NOT mention the words "context" or "document". Just give the direct answer.

### USER QUESTION
{question}

### DIRECT ANSWER
"""

response = generate_answer(prompt)

print("\nAnswer:")
print(response)