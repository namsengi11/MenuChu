class UI:
    def __init__(self) -> None:   
        self.affirmative = {"yes", "good", "o"}
        self.negative = {"no", "bad", "x"}
        self.recCnt = 0
    
    def takeInput(self):
        userInput = input()
        return userInput
    
    def takeAnswer(self):
        while True:
            userAnswer = input()
            if userAnswer in self.affirmative:
                print("We helped you find your choice in %i tries!" % self.recCnt)
                return True
            elif userAnswer in self.negative:
                return False
            else:
                print("To accept recommendation, please reply with ", self.affirmative, \
                    "\nTo disapprove, reply with ", self.negative)
    
    def proposeFood(self, food: str):
        self.recCnt += 1
        print("How about %s?" % food)

