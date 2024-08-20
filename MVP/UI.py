class UI:
    def __init__(self) -> None:   
        self.affirmative = {"yes", "good", "o"}
        self.negative = {"no", "bad", "x"}
    
    def takeInput(self):
        userInput = input()
        return userInput
    
    def takeAnswer(self):
        userAnswer = input()
        while True:
            if userAnswer in self.affirmative:
                return True
            elif userAnswer in self.negative:
                return False
            else:
                print("To accept recommendation, please reply with ", self.affirmative, \
                    "\nTo disapprove, reply with ", self.negative)
    
    def proposeFood(self, food: str):
        print("How about %s?" % food)

