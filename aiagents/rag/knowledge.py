from uuid import uuid4
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone,ServerlessSpec

class KnowledgeBase:

    def __init__(self, pinecone_api_key: str, index_name:str, model_name:str = "all-MiniLM-L6-v2"):
        self.pinecone_api_key = pinecone_api_key
        self.index_name = index_name
        self.vectors = []
        self.model = SentenceTransformer(model_name)
        self.pinecone = Pinecone(api_key=self.pinecone_api_key)

    def add_to_knowledgebase(self, vectors):
        try:
            existing_indexes = self.pinecone.list_indexes()
            index_names = [index['name'] for index in existing_indexes]
            if self.index_name not in index_names:
                self.pinecone.create_index(
                    name=self.index_name,
                    dimension=384,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )

            index = self.pinecone.Index(self.index_name)
            index.upsert(vectors=vectors)

            return None

        except Exception as e:
            raise Exception(f"An error occurred while setting up the Pinecone index: {e}")

    def get_vectors(self, chunks):
        for _, chunk in enumerate(chunks):
            embedding = self.model.encode(chunk['text'])
            metadata  = {
                "text" : chunk["text"]
            }
            self.vectors.append((str(uuid4()), embedding.tolist(), metadata))

        return None

    def extract_knowledge_base(self, query:str):
        index = self.pinecone.Index(self.index_name)
        query_embedding = self.model.encode(query)
        results = index.query(vector=query_embedding.tolist(), top_k=3)
        ids_to_fetch = [match['id'] for match in results['matches']]
        fetched_embeddings = index.fetch(ids=ids_to_fetch)
        fetched_chunks = [data.get("metadata") for id,data in fetched_embeddings["vectors"].items()]
        return [chunk["text"] for chunk in fetched_chunks]