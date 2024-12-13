## a separate tool to create RAG vectorstore. however, you can also 
## run ragged files at here and directly chat.

import os
from langchain_chroma import Chroma
# from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, JSONLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder

import json

import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from config import *

def load_directory_documents(directory_path):
    """Load documents from all files in a directory recursively."""
    # Using DirectoryLoader to recursively load all files in the directory
    text_loader = DirectoryLoader(
        directory_path,
        glob="**/*.*",  # Load all files
        show_progress=True,
        use_multithreading=True
    )
    docs = text_loader.load()
    return docs

def load_json_documents(json_path):
    """
        Load documents from a JSON file following llama-factory's fine-tuning type with:
        "instruction"
        "input"
        "output"
        where each entry using 'instruction' as entry.
    """
        # Define a metadata extraction function
    def metadata_func(record: dict, metadata: dict) -> dict:
        metadata["input"] = record.get("input")
        metadata["output"] = record.get("output")
        return metadata

    # Create a JSONLoader instance
    json_loader = JSONLoader(
        file_path=json_path,
        jq_schema='.[]',
        content_key="instruction",
        metadata_func=metadata_func
    )
    
    # aaa = json_loader.load()
    return json_loader.load()

def load_pdf_documents(pdf_path):
    """Load documents from a PDF file using PyPDFLoader."""
    pdf_loader = PyPDFLoader(pdf_path)
    return pdf_loader.load()

def generate_database(file_paths, db_dir):
    """
    Generate a vectorstore database from a list of file paths. Supports JSON and PDF files.
    
    Args:
        file_paths (list): List of file paths (JSON or PDF).
        db_dir (str): Directory to store the vector database.
        openai_api_key (str): OpenAI API key for embedding generation.
        openai_base_url (str): OpenAI base URL (optional).
    """
    # Initialize embeddings
    embedding = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=openai_api_key,
        base_url=openai_base_url
    )
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Load and split documents from each file
    all_splits = []
    for file_path in file_paths:
        path = Path(file_path)
        if path.is_dir():
            # Load all documents from the directory recursively
            documents = load_directory_documents(file_path)
        elif path.suffix.lower() == ".json":
            # Load JSON documents
            documents = load_json_documents(file_path)
        elif path.suffix.lower() == ".pdf":
            # Load PDF documents
            documents = load_pdf_documents(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            continue

        # Split the documents into smaller chunks
        splits = text_splitter.split_documents(documents)
        all_splits.extend(splits)
    
    # Create or load the vectorstore
    if not os.path.exists(db_dir):
        # Create a new vectorstore and persist it
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=embedding,
            persist_directory=db_dir
        )
        # vectorstore.persist()  # Save the vectorstore to disk, now automatically persisted
    else:
        # Load existing vectorstore from disk
        vectorstore = Chroma(
            embedding_function=embedding,
            persist_directory=db_dir
        )
    
    print(f"Database generated and saved at: {db_dir}")
    return vectorstore

def get_rag_model(db_dir):
    """Retrieve and configure the RAG model with the database."""
    # Initialize the language model (LLM)
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=deepseek_api_key,
        base_url=deepseek_base_url
    )

    # Initialize embeddings
    embedding = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=openai_api_key,
        base_url=openai_base_url
    )

    # Load the existing vectorstore from disk
    if os.path.exists(db_dir):
        vectorstore = Chroma(
            embedding_function=embedding,
            persist_directory=db_dir
        )
        print(f"Loaded vectorstore from: {db_dir}")
    else:
        raise FileNotFoundError(f"Database not found at {db_dir}")

    # Set up retriever
    retriever = vectorstore.as_retriever()

    # Define the RAG prompt
    prompt = PromptTemplate.from_template(
        """
        You should answer questions for users.
        Helpful message from retrieval tool: \n{context} \n
        Your task is: \n {question} \n
        """
    )

    # Set up the RAG inference chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

# Format retrieved documents for the LLM
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    # Define the directory containing the dataset
    dataset_directory = "/home/Agents4ICS/dataset/dataset_for_bm/oscat_plc_code_793.json"
    db_dir = "/home/lzh/work/Agents4ICS/database/st_db"
    # db_dir = "/home/Agents4ICS/databases"

    
    # # Generate the database from the given directory
    generate_database([dataset_directory], db_dir)
    
    # Load the RAG model
    rag_chain = get_rag_model(db_dir)

    # Chat function to interact with the RAG model
    def chat():
        print("RAG Chat - type 'exit' to quit")
        while True:
            question = input("You: ")
            if question.lower() == "exit":
                print("Goodbye!")
                break
            answer = rag_chain.invoke(question)
            print(f"RAG: {answer}")

    # Start the chat
    chat()