from modele.critere import Critere
class Numerique(Critere):
    def __init__(self, nom, poids):
        super().__init__(self, nom, poids)
        self.min = None
        self.max = None
    
    def definition_intervalle(self, valeur):
        if self.min is None or valeur < self.min:
            self.min = valeur
        if self.max is None or valeur > self.max:
            self.max = valeur
    def calcul_score(self, groupe):
        pass