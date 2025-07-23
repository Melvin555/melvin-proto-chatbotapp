#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:37:44 2025

@author: melvinharsono
"""

import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import pandas as pd

working_dir = "/Users/melvinharsono/Downloads/"

load_dotenv("/Users/melvinharsono/workingdirectory/environment/melvin_openai_cred.env")

required_env_vars = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_DEPLOYMENT",
    "AZURE_DEPLOYMENT_EMBEDDINGS",
]

missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


df = pd.read_excel(working_dir + "amaris_main_data.xlsx")
# Combine QUESTION and ANSWER columns into a single text column
df['CONTEXT'] = df['Question'] + " " + df['Answer']

# Save the CONTEXT column to a text file
with open(working_dir + 'amaris_main_text.txt', 'w', encoding='utf-8') as file:
    for context in df['CONTEXT']:
        file.write(context + '\n')



def create_vector_database(txt_path, chunk_size=5000):
    with open(txt_path, "r", encoding="utf-8") as file:
        data = file.read()
    
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_EMBEDDINGS"),
        openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    )
    
    faiss_dbs = []
    for idx, chunk in enumerate(chunks):
        chunk_path = f"{working_dir}chunk_{idx}.txt"
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        
        loader = TextLoader(chunk_path)
        docs = loader.load()
        documents = RecursiveCharacterTextSplitter(
            chunk_size=250, separators=["\n", "\n\n"], chunk_overlap=200
        ).split_documents(docs)
        
        db = FAISS.from_documents(documents=documents, embedding=embeddings)
        faiss_dbs.append(db)
    
    return faiss_dbs

def merge_faiss_databases(faiss_dbs, output_path):
    if not faiss_dbs:
        raise ValueError("No FAISS databases to merge.")
    
    merged_db = faiss_dbs[0]
    for db in faiss_dbs[1:]:
        merged_db.merge_from(db)
    
    merged_db.save_local(output_path)

if __name__ == "__main__":
    faiss_dbs = create_vector_database(working_dir+"amaris_main_text.txt", chunk_size=5000)
    merge_faiss_databases(faiss_dbs, working_dir+"amaris-faiss-db-output")
