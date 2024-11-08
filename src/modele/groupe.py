
class Groupe:
    def __init__(self, taille):
        self.taille = taille
        self.contraintes = {}  # Dictionnaire pour les contraintes
        self.eleves = set()

    def ajouter_contrainte(self, type_contrainte, liste_valeur):
        self.contraintes[type_contrainte] = liste_valeur
    
    def ajouter_eleve(self, eleve):
        self.eleves.add(eleve)
    
    def get_eleves(self):
        return self.eleves
    