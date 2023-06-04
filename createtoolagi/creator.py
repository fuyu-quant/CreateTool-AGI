from langchain.llms import OpenAI
import re


class Creator():
    def __init__(
        self,
        create_model,
        ):
        self.create_model = create_model

    def run(self, input, search_result, created_tool_code):
        print("> Create a tool.")

        related_tools = ''
        for i in range(len(search_result)):
            disc = search_result[i].payload['discription']
            code = search_result[i].payload['code']
            related_tools += 'discription:' + '\n' + disc +'\n' + 'code:' +'\n' + code + '\n' + '------------------' + '\n'



        create_prompt = """
        Please create your code in compliance with all of the following conditions.
        ・Create a python class that can execute {input_} with a single string as input.
        ・Output should be code only.
        ・Do not enclose the output in ``python ``` or the like.
        ・from langchain.tools import BaseTool must be written.
        ・Class must inherit from BaseTool.
        ・If you have previously created code that failed to execute, please refer to it as well.
        ・Here is the code I created previously: {created_tool_code_}
        
        ------------------
        {related_tools_}
        """.format(
            input_ = input, 
            created_tool_code_ = created_tool_code, 
            related_tools_ = related_tools
            )

        print(create_prompt)

        code = self.create_model(create_prompt)

        tool_name = re.search(r'name = "(.*?)"', code).group(1)


        print('\033[32m' + 'Completed!')
        print('Created tool name：' + tool_name + '\n' + '\033[0m')

        # Save to File
        #if folder_path_ != None:
        #    with open(folder_path_ + f'{name}.py', mode='w') as file:
        #        file.write(code)

        return code