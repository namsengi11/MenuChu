from Recommender import Recommender
from UI import UI

class Menuchu:
    def __init__(self):
        self.UI = UI()
        self.recommender = Recommender()

    def main(self):
        print("Having trouble choosing what to eat?")
        proposal = self.recommender.recRandomFood()
        self.UI.proposeFood(proposal)
        satisfied = False

        while not satisfied:
            answer = self.UI.takeAnswer()
            if answer:
                satisfied = True
            else:
                self.recommender.rejectFood(proposal)
                try:
                    proposal = self.recommender.recTopChoices()
                except Exception:
                    print("Restart Recommendation")
                    Menuchu().main()
                self.UI.proposeFood(proposal)

        print("I'm glad I found the right menu for you!!")

if __name__ == "__main__":
    Menuchu().main()

