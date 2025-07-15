# 🧭 Vector Indexing – Amaris Chatbot

This guide explains how we generate the FAISS vector index for the chatbot app.

---

## 🗂️ Dataset

We use an Excel file (`amaris_main_data.xlsx`) containing ~100 FAQ entries. Each row has:

- `Question`
- `Answer`

These are merged into a single `CONTEXT` field for chunking and embedding.

---

## 🛠️ Steps to Index

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare .env File
Ensure the following variables are defined:
```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=
AZURE_DEPLOYMENT_EMBEDDINGS=
```
### 3. Run the Indexing Script
```
python vector_indexing.py
```
This script will:

Combine questions and answers into one file

Chunk and split them into overlapping segments

Embed them using Azure OpenAI

Store them as a local FAISS vector database

🔁 Workflow Summary

Excel (Q&A) -> 
Merged into CONTEXT column -> 
Saved to Text File -> 
Chunked & Embedded -> 
Stored in FAISS DB

📁 Output Structure
```
amaris-faiss-db-output/
├── index.faiss
└── index.pkl
```
These files will be loaded in the chatbot to enable semantic retrieval.

⚙️ Chunk Settings
Outer chunk size: 5,000 characters

Inner chunk size: 250 characters with 200 character overlap

You can adjust these in create_vector_database() for better retrieval performance.

👨‍💻 Maintainer
Melvin Harsono
