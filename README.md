Markdown
# 🤖 NexusAI — Local Desktop AI Assistant

NexusAI is a fully self-contained, privacy-focused local AI desktop assistant built to run entirely on your local machine. By combining a quantized Large Language Model with a Retrieval-Augmented Generation (RAG) pipeline, NexusAI can securely chat, answer questions, and recall information from your private documents without a single byte of data leaving your computer.

---

## 🔹 Key Features

* **100% Local Execution:** No cloud dependencies, API keys, or internet connection required. Complete privacy for your personal data.
* **Knowledge Retrieval via RAG:** Knowledge retrieval pipeline powered by a vector database allows you to query your documents locally.
* **Modern Desktop GUI:** Clean, responsive, and intuitive graphical user interface featuring a secure login window and multi-line chat views.
* **Optimized Hardware Performance:** Powered by highly optimized quantized model inference designed to run smoothly on standard local environments.

---

## 🛠️ Technical Stack

* **Core Language:** Python
* **Frontend UI:** PySide6 (Qt for Python)
* **LLM Inference Engine:** Llama.cpp (`llama-cpp-python`)
* **Local LLM Model:** Qwen 2.5 3B Instruct (GGUF format, `Q4_K_M` quantization)
* **Vector Database (RAG):** ChromaDB
* **Backend Database:** SQLite (Handles user credentials and local session tracking)

---

## 📁 Repository Structure

```text
NEXUSAI/
│
├── Chat/                   # Chat pipeline managers
│   └── NexusChat.py        # Prompts and agentic orchestration rules
│
├── data/                   # Raw knowledge text/PDF source data documents
│
├── Frontend/               # PySide6 desktop interface components
│   ├── chat_window.py      # Core chat message interactions window
│   └── login.py            # User login and authorization window
│
├── LLM/                    # Local LLM initialization configs
│   └── model.py            # Llama.cpp inference & parameter settings
│
├── models/                 # Storage for local model weights
│   └── Qwen2.5-3B-Instruct-Q4_K_M.gguf
│
├── rag/                    # Chunking, embedding & retrieval pipelines
│   ├── NexusDB.py          # Vector database connector config
│   ├── RagEngine.py        # Core RAG retrieval engine logic
│   └── ragpipeline.py      # Embedding pipelines
│
├── vector_db/              # Persistent ChromaDB storage collection data
│
├── main.py                 # Application orchestrator launcher
├── Nexus_Chat_History.db   # SQLite application database file
├── Start_NexusAI.sh        # Double-click Linux execution shortcut script
└── requirements.txt        # Python dependency manifest

🚀 Getting Started (Xubuntu / Linux)
1. Prerequisites
Ensure you have Python 3, virtualenv, and build tools loaded on your system:

Bash
sudo apt update
sudo apt install python3-pip python3-venv build-essential

2. Installation & Setup
Navigate to the project root directory, activate your existing environment, and update the stack dependencies:

Bash
# Navigate to the project root directory
cd NEXUSAI

# Activate your local virtual environment
source NexusEnv/bin/activate

# Install the technical stack components
pip install -r requirements.txt

3. Launching the App
You can launch the program directly via your Xubuntu command line terminal or use the included automation shortcut script:

Via Terminal:

Bash
python3 main.py

Via Desktop GUI Double-Click Shortcut:

Grant the launcher script permission to execute:

Bash
chmod +x Start_NexusAI.sh
Double-click Start_NexusAI.sh inside your Thunar file manager to start the NexusAI application instantly!

🔒 Privacy & Optimization
Because this assistant relies heavily on local hardware constraints, configurations within LLM/model.py are set to n_threads=2 with a structured repeat_penalty=1.1 and customized ChatML stop sequence tags (<|im_end|>) to prevent infinite token loops, preserving battery life and lowering CPU overhead on Xubuntu environments.