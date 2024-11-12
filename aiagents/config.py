import os
from dotenv import load_dotenv

load_dotenv()
pinecone_api_key = os.getenv("pineconeapikey")
openai_api_key = os.getenv("openaiapikey")
mem0_api_key = os.getenv("mem0apikey")
index_name = "fueler"