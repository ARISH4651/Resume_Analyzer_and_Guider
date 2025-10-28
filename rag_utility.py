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


# loading the embedding model
embedding = HuggingFaceEmbeddings()

# load the llm form groq
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


def process_document_to_chroma_db(file_name):
    # load the doc using unstructured
    loader = UnstructuredPDFLoader(f"{working_dir}/{file_name}")
    documents = loader.load()
    
    # splitting te text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    # Sanitize metadata to ensure ChromaDB compatibility
    for doc in texts:
        if doc.metadata:
            # Remove None values and convert complex types to strings
            doc.metadata = {
                k: str(v) if v is not None else ""
                for k, v in doc.metadata.items()
                if isinstance(k, str) and k  # Only keep valid string keys
            }
    
    # Use ChromaDB with collection reset (avoid file locks on Windows)
    vectorstore_path = f"{working_dir}/doc_vectorstore"
    collection_name = "pdf_documents"
    
    # Try to delete existing collection by resetting it (safer than rmtree)
    try:
        import chromadb
        client = chromadb.PersistentClient(path=vectorstore_path)
        try:
            client.delete_collection(name=collection_name)
            print(f"Deleted existing collection: {collection_name}")
        except Exception:
            pass  # Collection doesn't exist yet
    except Exception as e:
        print(f"Could not reset collection: {e}")
    
    # Create new vectorstore
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embedding,
        persist_directory=vectorstore_path,
        collection_name=collection_name
    )
    
    # Try to persist and release any open handles
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

    # Verify data was stored
    print(f"Stored {len(texts)} chunks in ChromaDB")

    # release references and force GC to free files on Windows
    vectordb = None
    gc.collect()

    return 0


def answer_question(user_question):
    # load the persistent vectordb
    vectorstore_path = f"{working_dir}/doc_vectorstore"
    collection_name = "pdf_documents"
    
    vectordb = Chroma(
        persist_directory=vectorstore_path,
        embedding_function=embedding,
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
        llm=llm,
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