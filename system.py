from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import List, Tuple, Any
import os
import shutil


load_dotenv()

huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

template = """
User: You are an AI Assistant that follows instructions extremely well.
Please be truthful and give direct answers. Please tell 'I don't know' if user query is not in CONTEXT

Keep in mind, you will lose the job, if you answer out of CONTEXT questions


CONTEXT: {context}
Query: {question}

Remember only return AI answer
Assistant:
"""


def load_documents(documents: str) -> List[Any]:
    return PyPDFLoader(documents).load()


def chunking_nr_documents(docs: List[Any]) -> List[Any]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_documents(docs)


def embedding_and_vectorstore(texts: List[Any]) -> Tuple[FAISS, HuggingFaceBgeEmbeddings]:
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    hf = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    vectorstore = FAISS.from_documents(documents=texts, embedding=hf)

    return vectorstore, hf


def llm_and_chain(db: FAISS, query: str) -> str:
    retriever = db.as_retriever()

    llm = HuggingFaceEndpoint(
        repo_id="huggingfaceh4/zephyr-7b-alpha",
        max_new_tokens=512,
        repetition_penalty=1.1,
        temperature=0.2,
        top_p=0.5,
        return_full_text=False
    )

    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()

    chain = (
            {
                "context": retriever.with_config(run_name="Docs"),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | output_parser
    )

    answer = chain.invoke(query)

    return answer


def initialize_existing_db() -> Tuple[FAISS, HuggingFaceBgeEmbeddings]:
    db_file_path = "./faiss_index"

    print("loading database...")
    hf = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    db = FAISS.load_local(
        folder_path=db_file_path,
        embeddings=hf,
        index_name="index",
        allow_dangerous_deserialization=True
    )

    return db, hf


def creating_db(pdf_path: str) -> Tuple[FAISS, HuggingFaceBgeEmbeddings]:
    db_file_path = "./faiss_index"
    print("Creating database...")
    documents = load_documents(pdf_path)
    chunks = chunking_nr_documents(documents)
    db, hf = embedding_and_vectorstore(chunks)
    db.save_local(db_file_path)

    return db, hf


def delete_existing_db() -> None:
    print("deleting database...")
    db_file_path = "./faiss_index"

    if os.path.exists(db_file_path):
        shutil.rmtree(db_file_path)


def results(query: str) -> str:
    db, hf = initialize_existing_db()
    result = llm_and_chain(db, query)
    return result
