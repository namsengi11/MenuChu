import pandas as pd
import collections

class DBCleaner:
    def __init__(self, fileAddress) -> None:
        self.data = pd.read_csv(fileAddress)
        self.fileAddress = fileAddress
    
    def removeRepetition(self):
        cnt = collections.defaultdict(list)
        for idx, row in self.data.iterrows():
            cnt[row['Name']].append(idx)
        for food, idxs in cnt.items():
            while len(idxs) > 1:
                self.data.drop(idxs[1:], inplace=True)
                idxs.pop()
        self.data.to_csv(self.fileAddress, mode='w+', index=False )
        
if __name__ == "__main__":
    fileAddress = input("Enter File Address: ")
    DBCleaner(fileAddress).removeRepetition()