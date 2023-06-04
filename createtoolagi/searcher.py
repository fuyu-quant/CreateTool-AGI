from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from qdrant_client import QdrantClient

import re


class Searcher():
    def __init__(
        self,
        embedding_model,
        qdrant,
        ):
        self.embedding_model = embedding_model
        self.qdrant = qdrant

    def run(self, input):
        query = f"Helpful tools to do '{input}'"

        result = self.qdrant.search(
            collection_name="tool_store",
            query_vector = self.embedding_model.embed_query(query),
            limit=5
            )
            
        return result

    def save(self, tool_code):

        # Check the number of data included
        count = self.qdrant.count(collection_name = "tool_store", exact=True)
        idx = int(f'{count}'.replace('count=', '')) + 1

        tool_name = re.search(r'name = "(.*?)"', tool_code).group(1)
        description = re.search(r'description = "(.*?)"', tool_code).group(1)
        
        payload = {'discription': discription, 'code': tool_code, 'tool_name': tool_name}
        
        embedding = self.embedding_model.embed_query(discription)
        
        # upload data
        self.qdrant.upload_records(
            collection_name="tool_store",
            records=[models.Record(id=idx, vector=embedding, payload=payload)]
            )

        return