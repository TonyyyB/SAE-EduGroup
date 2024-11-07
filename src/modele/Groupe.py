
class Groupe:
    def __init__(self, taille):
        self.taille = taille
        self.contraintes = {}  # Dictionnaire pour les contraintes
        self.eleves = []

    def ajouterContrainte(self, type_contrainte, liste_valeur):
        self.contraintes[type_contrainte] = liste_valeur
    
    def ajouterEleve(self, eleve):
        self.eleves.append(eleve)
    