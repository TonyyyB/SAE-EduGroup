from modele.critere import Critere

class Categorique(Critere):
    def __init__(self, nom, poids):
        super().__init__(self, nom, poids)
        self.transposition_valeur = dict()
    def calcul_score(self, groupe):
        pass
        