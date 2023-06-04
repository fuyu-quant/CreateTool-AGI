from langchain.llms import OpenAI


class Decider():
    def __init__(
        self,
        base_model,
        ):
        self.base_model = base_model

    def run(self, input, search_result):
        print("> Decide if the task is executable.")
        
        executable_tasks = ''
        
        for i in range(len(search_result)):
            disc = search_result[i].payload['discription']
            code = search_result[i].payload['code']
            executable_tasks += 'discription:' + '\n' + disc +'\n' + 'code:' +'\n' + code + '\n' + '------------------' + '\n'

        prompt = """
        You are the agent who determines whether the input task can be executed.
        You execute tasks using the following tools. Please refer to the descriptions of the tools and the code to determine whether the task can be executed or not.
        The task you are to perform is {input_}.
        Answer "Yes." if you can perform the task, or "No." if you cannot.
        Do not output anything other than "Yes." or "No.".

        The following tools are available to you.
        -----------
        {executable_tasks_}
        
        """.format(input_ = input, executable_tasks_ = executable_tasks)

        responese = self.base_model(prompt)

        if responese == "Yes.":
            print('\033[32m' + 'I do not need to create a tool to run it.\n' + '\033[0m')

        elif responese == "No.":
            print('\033[32m' + 'I must create the tool before executing.\n' + '\033[0m')


        return responese