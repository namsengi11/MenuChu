import csv

class DBManager:
    def __init__(self) -> None:
        self.columns = []
        self.db = ['Flavor.csv', 'FoodType.csv']
        self.foods = dict()
        with open('FoodName.csv', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for food in reader:
                self.foods[int(food[0])] = food[1]

        for file in self.db:
            with open(file, newline='') as f:
                reader = csv.reader(f)
                self.columns.append(next(reader)[1:])
            
    def addFoodManually(self):
        # Take Name of Food
        name = input("Enter name of new food: ")

        print("Enter correct values for new food, between -1 and 1 for values")
        
        def promptFieldInput(fields):
            print("Enter corresponding value, distinguising each field with comma")
            userInput = input(', '.join(fields) + '\n')
            fileData = userInput.split(',')
            for field in fileData:
                if (float(field) < -1 or float(field) > 1):
                    print("Not in correct range")
                    return []
            return fileData

        data = []
        # Take user input for each characteristic category
        for columnIdx in range(len(self.db)):
            
            fileData = []
            # Request input for fields until its valid
            while not fileData:
                fileData = promptFieldInput(self.columns[columnIdx])
        
            userAnswer = input("To modify field, enter name of field. Else, enter \'x\': ")
            while userAnswer != 'x':
                fieldIdx = self.columns.index(userAnswer)
                newVal = input(self.columns[fieldIdx] + ": ")
                fileData[fieldIdx] = newVal
                userAnswer = input("To modify field, enter name of field. Else, enter \'x\'")
        
            data.append(fileData)
        
        newId = 0 if len(self.foods.keys()) == 0 else max(self.foods.keys()) + 1
        with open("FoodName.csv", "a", newline='') as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow([newId, name])
        for idx, fileData in enumerate(data):
            with open(self.db[idx], "a", newline='') as fp:
                wr = csv.writer(fp, dialect='excel')
                wr.writerow([newId] + fileData)

if __name__ == '__main__':
    DBManager().addFoodManually()