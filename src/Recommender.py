import random
import pandas as pd
import heapq

from numpy import dot
from numpy.linalg import norm

class Recommender:
    def __init__(self) -> None:
        self.foodPool = pd.read_csv('./FoodName.csv')
        self.foodFlavor = pd.read_csv('./Flavor.csv')
        self.foodType = pd.read_csv('./FoodType.csv')
        self.rejectedFlavorVector = pd.Series([0]*(len(self.foodFlavor.columns.drop('id'))), index=self.foodFlavor.columns.drop('id'))
        self.rejectedTypeVector = pd.Series([0]*(len(self.foodType.columns.drop('id'))), index=self.foodType.columns.drop('id'))
        # self.foodFlavor = pd.read_csv('./Flavor.csv').iloc[1:] 
        # self.foodType = pd.read_csv('./FoodType.csv').iloc[1:]
        self.rejectedCnt = 0
        self.rejectedFood = set()
        self.flavorWeight = 0.6
        self.typeWeight = 0.4


    def rejectFood(self, food: str):
        def adjustVectorAverage(vector, cnt, newVector):
            vector *= cnt
            vector += newVector
            vector /= cnt + 1
            return vector
        rejectedFoodId = int(self.foodPool[self.foodPool['Name'] == food]['id'].iloc[0])
        rejectedFoodFlavorV = self.foodFlavor[self.foodFlavor['id'] == rejectedFoodId].iloc[0].drop('id')
        rejectedFoodTypeV = self.foodType[self.foodType['id'] == rejectedFoodId].iloc[0].drop('id')

        # Recalculate vector representing rejected foods
        self.rejectedFlavorVector = adjustVectorAverage(self.rejectedFlavorVector, self.rejectedCnt, rejectedFoodFlavorV)
        self.rejectedTypeVector = adjustVectorAverage(self.rejectedTypeVector, self.rejectedCnt, rejectedFoodTypeV)

        self.rejectedCnt += 1
        self.rejectedFood.add(food)
        self.recalculateDist()

    def recalculateDist(self):
        # Calculate distances
        # Euclidean dist - what does axis do???
        # distances = self.numFoodPool.apply(lambda row: euclidean(self.rejectedVector, row), axis=1)

        # Cosine dist
        flavorDistances = self.foodFlavor.drop('id', axis=1) \
            .apply(lambda row: dot(row, self.rejectedFlavorVector)\
                    /(norm(row)*norm(self.rejectedFlavorVector)), axis=1)
        
        # for idx in self.foodType.index:
        #     df = self.foodType.drop('id', axis=1)
        #     print(idx, df.iloc[idx].to_frame().T, "\n", self.rejectedTypeVector.to_frame().T)
        #     print("dot: ", dot(df.iloc[idx],self.rejectedTypeVector))
        #     print("mag: ", norm(df.iloc[idx])*norm(self.rejectedTypeVector))

        typeDistances = self.foodType.drop('id', axis=1) \
            .apply(lambda row: dot(row, self.rejectedTypeVector)\
                    /(norm(row)*norm(self.rejectedTypeVector)), axis=1)

        # Add distances to the DataFrame
        self.foodPool['flavorDist'] = flavorDistances
        self.foodPool['typeDist'] = typeDistances

        # print(self.foodPool)

    def recTopChoices(self):
        pq = [] # Max Heap
        for index, row in self.foodPool.iterrows():
            dist = row['flavorDist'] * self.flavorWeight + row['typeDist'] * self.typeWeight
            if row['Name'] not in self.rejectedFood:
                if len(pq) < 3:
                    heapq.heappush(pq, (-dist, row['Name']))
                elif -pq[0][0] > -dist:
                    heapq.heapreplace(pq, (-dist, row['Name']))
        pq.sort()
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