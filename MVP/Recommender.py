import random
import pandas as pd
import heapq

from numpy import dot
from numpy.linalg import norm
from scipy.spatial.distance import euclidean

class Recommender:
    def __init__(self) -> None:
        self.foodPool = pd.read_csv('./data.csv')
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
        pq = []
        for index, row in self.foodPool.iterrows():
            if len(pq) < 5:
                heapq.heappush(pq, (-row['Distance'], row['Name']))
            elif pq[0][0] > -row['Distance']:
                heapq.heapreplace(pq, (-row['Distance'], row['Name']))
        print(self.rejectedVector)
        print(pq)
        options = [name for dist, name in pq]
        return self.recRandomFood(options)

    def recRandomFood(self, pool=None):
        recFood = ""
        if pool:
            randomIndex = random.randint(0, len(pool) - 1)
            recFood = pool[randomIndex]
        else: # Initial random recommendation without pool
            randomIndex = random.randint(0, len(self.foodPool) - 1)
            return self.foodPool.iloc[randomIndex]['Name']
        
        if recFood in self.rejectedFood:
            for food in pool:
                if food not in self.rejectedFood:
                    return food
            # All recommendations are not accepted, start again
            raise Exception("No suitable food, restart")
        else:
            return recFood