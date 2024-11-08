from modele.critere import Critere

class Booleen(Critere):
    def __init__(self, nom, poids):
        super().__init__(self, nom, poids)
    
    def calcul_score(self, groupe):
        pass
