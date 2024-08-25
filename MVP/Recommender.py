import random
import pandas as pd
import heapq

from numpy import dot
from numpy.linalg import norm

class Recommender:
    def __init__(self) -> None:
        self.foodPool = pd.read_csv('./data.csv')
        # self.foodPool = pd.read_csv('./testdata.csv')
        self.numFoodPool = self.foodPool.drop(columns=['Name'])
        self.rejectedVector = pd.Series([0]*(len(self.numFoodPool.columns)),index=self.numFoodPool.columns)
        self.rejectedCnt = 0
        self.rejectedFood = set()

    def rejectFood(self, food: str):
        self.rejectedVector *= self.rejectedCnt
        foodRow = self.foodPool[self.foodPool['Name'] == food]
        currRejectedFood = foodRow.iloc[0].drop(columns=['Names'])
        self.rejectedVector += currRejectedFood
        self.rejectedCnt += 1
        self.rejectedVector /= self.rejectedCnt
        self.rejectedFood.add(food)
        self.recalculateDist()

    def recalculateDist(self):
        # Calculate distances 
        # Euclidean dist - what does axis do???
        # distances = self.numFoodPool.apply(lambda row: euclidean(self.rejectedVector, row), axis=1)

        # Cosine dist
        distances = self.numFoodPool.apply(lambda row: dot(row, self.rejectedVector) \
                                           /(norm(row)*norm(self.rejectedVector)), axis=1)

        # Add distances to the DataFrame
        self.foodPool['Distance'] = distances
        print(self.foodPool)
    
    def recTopChoices(self):
        pq = [] # Max Heap
        for index, row in self.foodPool.iterrows():
            if row['Name'] not in self.rejectedFood:
                if len(pq) < 3:
                    heapq.heappush(pq, (-row['Distance'], row['Name']))
                elif -pq[0][0] > -row['Distance']:
                    heapq.heapreplace(pq, (-row['Distance'], row['Name']))
        pq.sort()
        print(pq)
        options = [name for dist, name in pq]
        if len(options) < 3:
            raise Exception("No suitable food, restart")
        return self.recRandomFood(options)

    def recRandomFood(self, pool=None):
        recFood = ""
        if pool:
            randomIndex = random.randint(0, 2 * len(pool) - 1)
            if randomIndex > len(pool):
                recFood = pool[-1]
            elif randomIndex > len(pool) // 2:
                recFood = pool[-2]
            else:
                recFood = pool[-3]
            
        else: # Initial random recommendation without pool
            randomIndex = random.randint(0, len(self.foodPool) - 1)
            return self.foodPool.iloc[randomIndex]['Name']
        
        if recFood in self.rejectedFood:
            for food in pool[::-1]:
                if food not in self.rejectedFood:
                    return food
            # All recommendations are not accepted, start again
            raise Exception("No suitable food, restart")
        else:
            return recFood