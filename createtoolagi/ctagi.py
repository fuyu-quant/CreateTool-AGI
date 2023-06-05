from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from qdrant_client import QdrantClient
from qdrant_client import models

from .creator import Creator
from .decider import Decider
from .executor import Executor
from .searcher import Searcher
from .planner import Planner


import traceback


class CTAGI():
    def __init__(
        self,
        base_model_name,
        create_model_name,
        embegging_model_name,
        qdrant,
        ):
        self.base_model_name = base_model_name
        self.base_model = OpenAI(temperature=0, model_name = self.base_model_name)

        self.create_model_name = create_model_name
        self.create_model = OpenAI(temperature=0, model_name = self.create_model_name)

        self.embegging_model_name = embegging_model_name
        self.embegging_model = OpenAIEmbeddings(model = self.embegging_model_name)

        self.input = input

        self.qdrant = qdrant
        #self.qdrant = QdrantClient(path='./tools')
        #self.qdrant.create_collection(collection_name ="tool_store", vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))

        self.planner = Planner(base_model = self.base_model)
        self.searcher = Searcher(embedding_model = self.embegging_model, qdrant = self.qdrant)
        self.decider = Decider(base_model = self.base_model)
        self.creator = Creator(create_model = self.create_model)
        self.executor = Executor(base_model = self.base_model)



    def run(self, input):
        #generalized_input = self.planner.run(input)
        generalized_input = input

        search_result = self.searcher.run(generalized_input)

        decision = self.decider.run(generalized_input, search_result = search_result)

        if decision == "Yes.":
            self.executor.run(input, search_result = search_result)

        #else:
        elif decision == "No.":
            count = 0
            created_tool_code = None
            while count < 10:
                count += 1
                print(f'Try:{count}')
                try:
                    tool_code = self.creator.run(generalized_input, search_result = search_result, created_tool_code = created_tool_code)
                    created_tool_code = tool_code

                    print(f"Created tool code: {tool_code}")
            
                    self.executor.run_with_create_tool(input, tool_code = tool_code)
                    
                    self.searcher.save(tool_code = tool_code)
                    break
                except Exception as e:
                    print('\033[32m' + f"Error occurred: {e}" + '\n' + '\033[0m')
                    traceback.print_exc()
                    
            if count >= 5:
                print('\033[32m' + "Reached the maximum number of tries." + '\033[0m')

            
        return 