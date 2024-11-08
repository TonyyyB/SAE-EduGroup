class Critere:
    
    def __init__(self, nom, poids):
        self.nom = nom
        self.poids = poids
        self.list_valeurs = []

    def ajouter_valeur(self, valeur):
        if valeur not in self.list_valeurs:
            self.list_valeurs.append(valeur)

    def set_poids(self, poids):
        self.poids = poids
    
    def get_poids(self):
        return self.poids
    
    def get_nom(self):
        return self.nom
    