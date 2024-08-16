import random

class Recommender:
    def __init__(self) -> None:
        self.foodPool = ["kimchi", "chicken", "bahkuhteh", "chili crab", "bulgogi"]


    def rejectFood(self, food):
        pass
    
    def recRandomFood(self):
        randomIndex = random.randint(0, len(self.foodPool) - 1)
        return self.foodPool[randomIndex]