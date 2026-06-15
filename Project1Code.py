import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
import re
import os
import random
from rank_bm25 import BM25Okapi


def document_ingestion(path_dir):
    if path_dir is None: return []

    path_dir = Path(path_dir)
    if not path_dir.is_dir():
        print("Not a Valid Directory")
        return []

    documents = []
    for spec_file_path in Path(path_dir).glob("*.txt"): #Path makes an object that represents the directory, glob goes through this object and returns files following this REGex 
        with open(spec_file_path, "r", encoding="utf-8") as file:
            text = file.read()
            source_url = re.search(r"\[source:\s*(.*?)\]", text).group(1) #use regex to locate the neccessary metadata
            source_type = re.search(r"\[source_type:\s*(.*?)\]", text).group(1)
            course = re.search(r"\[Course:\s*(.*?)\]", text).group(1)
            body = re.sub(r"^\[source:.*?\]\s*\n\[source_type:.*?\]\s*\n\[Course:.*?\]\s*\n?","",text) #use regex to replace it and avoid it being in the chunks
            documents.append( Document(page_content=body , metadata={"source_file" :spec_file_path.name, "source_url": source_url, "source_type":source_type, "course": course}))
    return documents

def chunking_stage(documents,req_separators=["\n","\n\n"], chunk_size: int = 400, chunk_overlap: int = 20):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        separators= req_separators
    )
    final_split = []
    for single_document in documents:
        meta_data = single_document.metadata

        if meta_data.get("source_type", "").strip() == "RateMyProfessor":
            text_list = re.split(r"(?=Professor:)", single_document.page_content)
            final_split.extend([Document(page_content=text.strip() , metadata=meta_data) for text in text_list if text.strip()])
        else:
            final_split.extend(text_splitter.split_documents([single_document]))

    return final_split

def embeding_storing(chunks_to_use):

    CHROMA_PATH = r"chroma_db"
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        chroma_client.delete_collection("UIUC_CS_Class_Information")
    except:
        pass
    collection = chroma_client.get_or_create_collection(name="UIUC_CS_Class_Information")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    text = [chunk.page_content for chunk in chunks_to_use]
    embeddings = model.encode(text).tolist()
    meta_data = [chunk.metadata for chunk in chunks_to_use]
    collection.add(documents=text,metadatas=meta_data,embeddings=embeddings,ids=[str(i) for i in range(len(chunks_to_use))])

def request_query(query,bm25,chunks,topk: int = 3):
    query_embedding = SentenceTransformer("all-MiniLM-L6-v2").encode(query).tolist()

    CHROMA_PATH = r"chroma_db"
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name="UIUC_CS_Class_Information")
    
    results = collection.query(query_embeddings=[query_embedding],n_results=7)
    bm25_scoring = bm25.get_scores(query.lower().split())
    max_bm25 = max(bm25_scoring) if max(bm25_scoring) > 0 else 1

    new_scoring = []
    for i in range(len(results["ids"][0])):
        idx = int((results["ids"][0])[i])
        sim = 1 / (1 + results["distances"][0][i])
        bm25_normalized = bm25_scoring[idx] / max_bm25
        new_calc = (0.4 * sim) + (0.6 * bm25_normalized)
        
        new_scoring.append({"scoring": new_calc, "id" : idx})

    sorted_by_score = sorted(new_scoring, key=lambda x:x["scoring"],reverse=True)

    final_results = []
    for item in sorted_by_score[:3]:
        idx = item["id"]
        final_results.append((item["scoring"], (chunks[idx]).page_content, (chunks[idx]).metadata))
    

    return final_results

def prompting(top_chunks,query):
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")

    system_prompt = """
    You are a helpful college advisor who also attended the computer science program at the Univerity of Illinois at Urbana Champaign. You answer questions regarding courses within the computer science program at UIUC with information that only students or experienced people would know.
    You only answer based on the knowledge I will provided after the context key word. You don't make up any information and if you don't know, you simply respond that you do not know. With each response, you must provide textual evidence and reference where the source was from. If you do no respect any one of these rules, the user will fail at making their decision, lose their full-ride scholarship, and they will live a miserable life.
    Your ability to respond is crucial to the user not living a terrible and sad life.

    -----------------------------------------------
    context:
    """
    for i in range(len(top_chunks)):
        source_name = "source:" + str(((top_chunks[i])[2])["source_file"])
        source_url = "source_url:" + str(((top_chunks[i])[2])["source_url"])
        system_prompt += '\n' 
        system_prompt += source_name
        system_prompt += '\n'
        system_prompt += source_url
        system_prompt += str(((top_chunks[i])[1]))
    
    system_prompt += "\n"
    system_prompt += "query: "
    system_prompt += str(query)

    client = Groq(api_key=groq_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages= [
            {
                "role":"user",
                "content": system_prompt
            }
        ]
    )
    print(response.choices[0].message.content)


current_path_directory = "documents"
docs = document_ingestion(current_path_directory)
chunks = chunking_stage(docs,req_separators=[
        "\nProfessor:",
        "\ncomment:",
        "\n\n",
        "\n",
        " ",
        ""
        ],chunk_size=400,chunk_overlap=20)

texts = [c.page_content for c in chunks]
tokenized_texts = [t.lower().split() for t in texts]
bm25 = BM25Okapi(tokenized_texts)



query = "Which professor is know for their skatboarding ability among students?"
#print(len(chunks))
embeding_storing(chunks_to_use=chunks)
results = request_query(query=query,bm25=bm25,chunks=chunks)

for i in range(len(results)):
    print(results[i])
    print("-" * 80)

print("\n")
print("\n")
prompting(results,query)
