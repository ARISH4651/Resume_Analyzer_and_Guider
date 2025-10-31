import os
import json
import shutil
import time
import gc
import logging

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA


working_dir = os.path.dirname(os.path.abspath((__file__)))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# Lazy loading for embedding model and llm
_embedding = None
_llm = None

def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = HuggingFaceEmbeddings()
    return _embedding

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )
    return _llm


def process_document_to_chroma_db(file_name):
    # load the doc using unstructured
    loader = UnstructuredPDFLoader(f"{working_dir}/{file_name}")
    documents = loader.load()
    
    # Add file metadata to each document
    import time
    start_total = time.time()

    print(f"[TIMER] Starting processing for {file_name}")
    start_load = time.time()
    loader = UnstructuredPDFLoader(f"{working_dir}/{file_name}")
    documents = loader.load()
    print(f"[TIMER] Document load time: {time.time() - start_load:.2f}s")

    start_split = time.time()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    print(f"[TIMER] Text splitting time: {time.time() - start_split:.2f}s")

    start_sanitize = time.time()
    for doc in texts:
        if doc.metadata:
            doc.metadata = {
                k: str(v) if v is not None else ""
                for k, v in doc.metadata.items()
                if isinstance(k, str) and k
            }
    print(f"[TIMER] Metadata sanitization time: {time.time() - start_sanitize:.2f}s")

    start_vector = time.time()
    vectorstore_path = f"{working_dir}/doc_vectorstore"
    collection_name = "pdf_documents"
    try:
        vectordb = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=get_embedding(),
            collection_name=collection_name
        )
        vectordb.add_documents(texts)
        print(f"Added {len(texts)} chunks from {file_name} to existing ChromaDB collection")
    except Exception:
        print(f"Creating new ChromaDB collection for {file_name}")
        vectordb = Chroma.from_documents(
            documents=texts,
            embedding=get_embedding(),
            persist_directory=vectorstore_path,
            collection_name=collection_name
        )
    print(f"[TIMER] Vectorstore time: {time.time() - start_vector:.2f}s")

    start_persist = time.time()
    try:
        if hasattr(vectordb, "persist"):
            try:
                vectordb.persist()
            except Exception:
                pass
        client = getattr(vectordb, "client", None)
        if client is not None and hasattr(client, "shutdown"):
            try:
                client.shutdown()
            except Exception:
                pass
    except Exception:
        pass
    print(f"[TIMER] Persist/shutdown time: {time.time() - start_persist:.2f}s")

    print(f"[TIMER] Total processing time for {file_name}: {time.time() - start_total:.2f}s")

    vectordb = None
    gc.collect()
    return 0

def answer_question(user_question):
    # load the persistent vectordb
    vectorstore_path = f"{working_dir}/doc_vectorstore"
    collection_name = "pdf_documents"
    
    vectordb = Chroma(
        persist_directory=vectorstore_path,
        embedding_function=get_embedding(),
        collection_name=collection_name
    )
    
    # retriever with more documents
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Retrieve top 5 most relevant chunks
    )
    
    # Debug: Check what documents are retrieved
    retrieved_docs = retriever.get_relevant_documents(user_question)
    print(f"Retrieved {len(retrieved_docs)} documents for question: {user_question}")
    if retrieved_docs:
        print(f"First retrieved chunk preview: {retrieved_docs[0].page_content[:200]}...")

    # create a chain to answer user question using Groq
    qa_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    response = qa_chain.invoke({"query": user_question})
    # langchain may return a dict or string depending on version
    if isinstance(response, dict):
        answer = response.get("result") or response.get("answer") or response.get("output")
    else:
        answer = response

    # cleanup vectordb resources
    try:
        client = getattr(vectordb, "client", None)
        if client is not None and hasattr(client, "shutdown"):
            try:
                client.shutdown()
            except Exception:
                pass
    except Exception:
        pass

    vectordb = None
    gc.collect()

    return answer