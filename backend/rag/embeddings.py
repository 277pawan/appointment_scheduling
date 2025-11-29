from google import genai 
from dotenv import load_dotenv
load_dotenv()
import os 
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

client=genai.Client(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return resp.data[0].embedding

