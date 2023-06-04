from langchain.llms import OpenAI


class Decider():
    def __init__(
        self,
        base_model,
        ):
        self.base_model = base_model

    def run(self, input, search_result):
        
        executable_tasks = ''
        
        for i in range(len(search_result)):
            disc = search_result[i].payload['discription']
            code = search_result[i].payload['code']
            
        executable_tasks += 'discription:' + '\n' + disc +'\n' + 'code:' +'\n' + code + '\n' + '------------------' + '\n'

        prompt = """
        You are the agent that determines if the input task is executable.
        Please check the description in the "Task" field and the main processing part of the code to be executed, and decide if the task is executable.
        The task you are to perform is {input_}.
        Answer "Yes." if you can perform the task, or "No." if you cannot.
        Do not output anything other than "Yes." or "No.".

        What you can do is described below.         
        -----------
        {executable_tasks_}
        
        """.format(input_ = input, executable_tasks_ = executable_tasks)

        responese = self.base_model(prompt)

        if responese == "Yes.":
            print('\033[32m' + 'I do not need to create a tool to run it.\n' + '\033[0m')

        elif responese == "No.":
            print('\033[32m' + 'I must create the tool before executing.\n' + '\033[0m')


        return responese