import csv

class DBManager:
    def __init__(self) -> None:
        self.columns = []
        with open('data.csv', newline='') as f:
            reader = csv.reader(f)
            self.columns = next(reader)

    def addFoodManually(self):
        print("Enter correct value for new food, between -1 and 1 for values")
        data = []
        for col in self.columns:
            newCol = input(col + ": ")
            while col != "Name" and (float(newCol) < -1 or float(newCol) > 1):
                print("Not in correct range")
                newCol = input(col + ": ")
            data.append(newCol)
        
        userAnswer = input("To modify field, enter name of field. Else, enter \'x\': ")
        while userAnswer != 'x':
            fieldIdx = self.columns.index(userAnswer)
            newVal = input(self.columns[fieldIdx] + ": ")
            data[fieldIdx] = newVal

            userAnswer = input("To modify field, enter name of field. Else, enter \'x\'")

        with open("data.csv", "a", newline='') as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(data)

if __name__ == '__main__':
    DBManager().addFoodManually()