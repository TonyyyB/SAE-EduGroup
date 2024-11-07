import TypeCritere

class Cat(TypeCritere.TypeCritere):
        
        def __init__(self, nom, poids):
            TypeCritere.TypeCritere.__init__(self, nom, poids)
            self.transposition_valeur = dict()
        