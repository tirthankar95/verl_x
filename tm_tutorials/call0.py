from typing import List 

class Queue:
    def __init__(self, x: List[int]):
        self.arr = x 
    def __call__(self, factor):
        res = [factor * x for x in self.arr]
        return res 

multiply = Queue([i+1 for i in range(10)])
print(multiply(2))