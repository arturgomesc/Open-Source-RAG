# Open Source RAG 🤗🦜

## Here's how you upload your files and ask him questions with Python, Langchain and HuggingFace, free of charge!

This project implements a Retrieval-Augmented Generation (RAG) system using user-uploaded PDF documents. The system allows the user to upload a PDF document and ask questions based on the content of the document. When a new PDF is uploaded, the system replaces the old document and recreates the vector database.

## Frameworks and libraries

* Langchain 🦜🔗: to NLP tasks
* Hugging Face 🤗: where the embedding model and LLM comes. We are using [bge-small-en](https://huggingface.co/BAAI/bge-small-en) to embedding and [zephyr-7b-alpha](https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha) to LLM
* FAISS 📊: open-source vector database
* PyPDF 📄: to load the PDF files
* Streamlit 🔴: to view our application
* Docker 🐋: containerize our system

## Running the Application with Docker

### Prerequisites

* Docker installed on your machine.

## Building and Running the Docker Container

### Clone the Repository:

``` 
git clone https://github.com/arturgomesc/rag-open-source-system.git
cd rag-open-source-system
```

### Create a .env File:
