````md
# LexMind — AI Legal Research Assistant

## Overview

LexMind is an AI-powered Legal Research and Case Analysis platform designed to assist legal professionals in analyzing case documents using Retrieval-Augmented Generation (RAG). The system combines semantic search, vector databases, document retrieval, and large language models to generate grounded legal insights from uploaded case files.

The platform enables users to upload legal PDFs, retrieve semantically relevant evidence, identify applicable legal sections, and generate structured legal summaries based strictly on retrieved context.

This project was developed as an end-to-end AI engineering and applied NLP system focusing on practical legal-document intelligence workflows.

---

# Core Features

- Upload and process legal case PDFs
- Automatic document chunking and indexing
- Semantic retrieval using transformer embeddings
- Vector similarity search with Qdrant
- Retrieval-Augmented Generation (RAG) pipeline
- Evidence-grounded legal summarization
- Relevant IPC section identification
- Witness and evidence extraction
- Confidence score estimation
- Interactive conversational legal assistant
- Professional Streamlit-based interface
- Cloud deployment support using Streamlit Community Cloud

---

# Problem Statement

Legal case documents are often lengthy, unstructured, and difficult to analyze efficiently. Lawyers and legal researchers spend significant time manually identifying critical evidence, relevant witness statements, and applicable legal provisions.

LexMind addresses this problem by creating an AI-assisted legal retrieval system capable of:

- Understanding uploaded legal documents semantically
- Retrieving the most relevant evidence for a query
- Producing grounded legal summaries
- Mapping facts to applicable IPC sections
- Reducing manual document review effort

---

# System Architecture

The system follows a Retrieval-Augmented Generation (RAG) architecture.

## Workflow

```text
PDF Upload
    ↓
Text Extraction
    ↓
Document Chunking
    ↓
Sentence Embedding Generation
    ↓
Vector Storage in Qdrant
    ↓
Semantic Similarity Retrieval
    ↓
Context Assembly
    ↓
LLM-based Legal Reasoning
    ↓
Structured Legal Response
````

---

# AI Pipeline

## 1. PDF Processing

Uploaded legal PDFs are parsed using `pdfplumber`.

The extracted text is:

* cleaned
* segmented
* divided into semantically meaningful chunks

Each chunk is associated with:

* page number
* case identifier
* metadata

---

## 2. Embedding Generation

The project uses:

```text
BAAI/bge-small-en-v1.5
```

from Sentence Transformers for semantic embedding generation.

The embedding model converts each document chunk into dense vector representations suitable for semantic retrieval.

---

## 3. Vector Database

Qdrant is used as the vector database.

Responsibilities:

* storing embeddings
* similarity search
* semantic retrieval
* metadata filtering

The database retrieves the most relevant chunks based on cosine similarity.

---

## 4. Retrieval-Augmented Generation (RAG)

When a user asks a legal question:

1. The query is embedded
2. Relevant evidence chunks are retrieved
3. Retrieved evidence is passed to the LLM
4. The LLM generates grounded legal analysis

This minimizes hallucination and improves factual consistency.

---

## 5. Legal Reasoning Layer

The system generates:

* legal summaries
* relevant IPC sections
* case-document insights
* short explanations

The model is instructed to:

* use only retrieved evidence
* avoid unsupported assumptions
* produce professional legal responses

---

# User Interface

The interface is built using Streamlit.

## Features

### Sidebar Workspace

* Lawyer ID management
* Case ID creation
* PDF upload workflow
* Document indexing

### Conversational Interface

* Interactive legal Q&A
* Multi-turn chat workflow
* Structured legal outputs

### Evidence Visualization

* Retrieved evidence panels
* Similarity score display
* Page-wise document traceability

### Confidence Estimation

* Retrieval-based confidence scoring
* Visual confidence indicators

---

# Technology Stack

| Category              | Technology                |
| --------------------- | ------------------------- |
| Frontend              | Streamlit                 |
| Language              | Python                    |
| Embeddings            | Sentence Transformers     |
| Embedding Model       | BAAI/bge-small-en-v1.5    |
| Vector Database       | Qdrant                    |
| LLM Provider          | OpenRouter                |
| PDF Parsing           | pdfplumber                |
| Numerical Processing  | NumPy                     |
| Deep Learning Backend | PyTorch                   |
| Transformer Framework | Hugging Face Transformers |

---

# Project Structure

```text
LexMind/
│
├── .streamlit/
│   └── secrets.toml
│
├── data/
│
├── LexMind_RAG_Legal_Assistant.ipynb
│
├── streamlit_app.py
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/LexMind-AI-Legal-Assistant.git
```

```bash
cd LexMind-AI-Legal-Assistant
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
OPENROUTER_API_KEY = "your_openrouter_api_key"
```

---

# Running the Application

## Local Execution

```bash
streamlit run streamlit_app.py
```

The application will launch locally at:

```text
http://localhost:8501
```

---

# Deployment

The application is designed for deployment using:

* Streamlit Community Cloud

Deployment workflow:

1. Push repository to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets
4. Deploy `streamlit_app.py`

---

# Example Capabilities

## Legal Summarization

```text
Summarize the incident in simple legal language.
```

---

## IPC Mapping

```text
Which IPC sections may apply in this case?
```

---

## Evidence Extraction

```text
What evidence was collected from the crime scene?
```

---

## Witness Analysis

```text
List all witness statements.
```

---

## Legal Reasoning

```text
Generate prosecution arguments based on the evidence.
```

---

# Sample Output Structure

The system generates responses in the following structure:

* Legal Summary
* Relevant Sections
* Case-document Insights
* Short Explanation
* Confidence Score
* Retrieved Evidence

---

# Engineering Highlights

* End-to-end RAG pipeline implementation
* Semantic search over legal documents
* Evidence-grounded response generation
* Vector database integration
* Transformer-based embeddings
* Production-style AI application workflow
* Interactive conversational interface
* Cloud deployment pipeline

---

# Research and Learning Areas Covered

This project demonstrates practical understanding of:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Transformer Embeddings
* Prompt Engineering
* Information Retrieval
* Applied NLP
* LLM Integration
* AI Product Engineering
* Conversational AI Systems

---

# Author

Raj Aryan

---

# License

This project is intended for educational, research, and portfolio purposes.

```
```
