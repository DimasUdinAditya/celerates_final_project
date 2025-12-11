# Starbucks Customer Service Chatbot

Chatbot RAG-based untuk customer service Starbucks menggunakan Gemini, Langchain, dan Qdrant.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup environment variables:
```bash
cp .env.example .env
# Edit .env dan masukkan API keys
```

3. Setup vector database:
```bash
python scripts/setup_vectorstore.py
```

4. Ingest documents:
```bash
# Letakkan file PDF di folder data/raw/
python scripts/ingest_documents.py
```

5. Run aplikasi:
```bash
python run.py
# atau
streamlit run app/streamlit_app.py
```

## Struktur Proyek

- `src/` - Core logic dan komponen
- `app/` - Streamlit UI
- `scripts/` - Utility scripts
- `data/` - Dokumen PDF
- `tests/` - Unit tests

## Teknologi

- Langchain
- Google Gemini (LLM & Embeddings)
- Qdrant (Vector Database)
- Streamlit (UI)
