from modele.type_critere import TypeCritere
class Numerique(TypeCritere):
        
        def __init__(self, nom, poids):
            super().__init__(self, nom, poids)
            self.min = None
            self.max = None
        
        def definition_intervalle(self, valeur):
            if self.min is None or valeur < self.min:
                self.min = valeur
            if self.max is None or valeur > self.max:
                self.max = valeur