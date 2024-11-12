from config import pinecone_api_key, index_name
from rag import KnowledgeBase, DocumentLoader, DocumentSplitter

dataloader = DocumentLoader(r"data\knowledgebase.txt")
data = dataloader.load_data()
splitter = DocumentSplitter(data)
chunks = splitter.split_data()
knowledgebase = KnowledgeBase(pinecone_api_key=pinecone_api_key,index_name=index_name)
knowledgebase.get_vectors(chunks)
knowledgebase.add_to_knowledgebase(knowledgebase.vectors)