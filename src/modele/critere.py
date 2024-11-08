
class Critere:

    def __init__(self, type_critere, valeur):
        self.type_critere = type_critere
        self.valeur = valeur
        self.type_critere.ajouter_valeur(valeur)
    
    def get_type_critere(self):
        return self.type_critere
    
    def get_valeur(self):
        return self.valeur
    