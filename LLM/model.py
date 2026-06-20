from llama_cpp import Llama

MODEL_PATH = "models/Qwen2.5-3B-Instruct-Q4_K_M.gguf"

print("Loading NEXUSAI...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=2,
    verbose=False
)

print("Model loaded successfully!")


def generate_answer(prompt):
    response = llm(
        prompt,
        max_tokens=256,
        stop=["###", "\n\n"],
        temperature=0.3
    )

    return response["choices"][0]["text"].strip()