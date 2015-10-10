
class Card:
    def __init__(self, category, title, link):
        self.category = category
        self.title = title
        self.link = link
        
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(tuple(self))
