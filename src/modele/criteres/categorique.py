from modele.type_critere import TypeCritere

class Categorique(TypeCritere):
        def __init__(self, nom, poids):
            super().__init__(self, nom, poids)
            self.transposition_valeur = dict()
        