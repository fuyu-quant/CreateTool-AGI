from langchain.tools import BaseTool

class SumOfPrimesTool(BaseTool):
    name = "SumOfPrimesTool"
    description = "used for calculating the sum of prime numbers from A to B. The input is a single string with two numbers separated by a comma. For example, if you want to find the sum of prime numbers between 2 and 10, the input is '2,10'."

    def is_prime(self, num: int) -> bool:
        "Check if a number is prime."
        if num < 2:
            return False
        for i in range(2, num):
            if num % i == 0:
                return False
        return True

    def _run(self, query: str) -> str:
        "Use the tool."
        a, b = query.split(",")
        a, b = int(a), int(b)
        prime_sum = sum([x for x in range(a, b + 1) if self.is_prime(x)])
        return prime_sum

    async def _arun(self, query: str) -> str:
        "Use the tool asynchronously."
        raise NotImplementedError("SumOfPrimesTool does not support async")