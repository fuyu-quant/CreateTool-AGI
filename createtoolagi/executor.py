from langchain.llms import OpenAI
from langchain.agents import initialize_agent

import re


class Executor():
    def __init__(
        self,
        base_model,
        ):
        self.base_model = base_model

    def run(self, input, search_result):
        print("> Execute the task.")

        tools = []

        for i in range(len(search_result)):
            disc = search_result[i].payload['discription']
            code = search_result[i].payload['code']
            tool_name = search_result[i].payload['tool_name']

            tool_code = code + '\n' + f'{tool_name} = {tool_name}()'
            exec(tool_code, globals())
            exec(f'tools.append({tool_name})', globals())

        agent = initialize_agent(
            tools, 
            self.base_model, 
            agent="zero-shot-react-description", 
            verbose=True
            )

        agent.run(input)

        return

    def run_with_create_tool(self, input, tool_code):
        print("> Execute the task with the tool you created.")

        tools = []

        tool_name = re.search(r'name = "(.*?)"', tool_code).group(1)

        tool_code = tool_code + '\n' + f'{tool_name} = {tool_name}()'
        exec(tool_code, globals())
        exec(f'tools.append({tool_name})', globals())

        agent = initialize_agent(
            tools, 
            self.base_model, 
            agent="zero-shot-react-description", 
            verbose=True
            )

        agent.run(input)

        return