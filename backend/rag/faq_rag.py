import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import OpenAI
from .vector_store import add_documents, query_collection, get_collection
from google import genai

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client=genai.Client(api_key=GEMINI_API_KEY)

DATA_PATH = "data/clinic_info.json"


def ingest_faq():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    idx = 0
    for section, items in data.items():
        for item in items:
            text = f"{section}: {item['question']} - {item['answer']}"
            docs.append(
                {
                    "id": f"faq-{idx}",
                    "text": text,
                    "meta": {"section": section, "question": item["question"]},
                }
            )
            idx += 1
    add_documents(docs)

def answer_faq(query: str) -> str:
    # lazy ingest if empty
    if len(get_collection().peek()["ids"]) == 0:
        ingest_faq()

    # results = query_collection(query)
    # context = "\n".join([d for d, _ in results])


    prompt = f"""
You are a helpful clinic assistant. Use ONLY the context to answer.

Question: {query}

Answer briefly and clearly.
"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.5,
        google_api_key=os.getenv("GEMINI_API_KEY"),  # IMPORTANT FIX
    )

    response = llm.invoke(prompt)

    return response.content.strip()

