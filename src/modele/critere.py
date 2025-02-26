class Critere:
    def __init__(self, nom:str, poids:int, valeurs:set[str]=set()):
        self.nom:str = nom
        self.poids:int = poids
        self.valeurs:set[str] = valeurs

    def ajouter_valeur(self, valeur:str) -> None:
        self.valeurs.add(valeur)

    def set_poids(self, poids:int) -> None:
        self.poids:int = poids

    def get_poids(self) -> int:
        return self.poids

    def get_nom(self) -> str:
        return self.nom
    
    def get_valeurs(self) -> set[str]:
        return self.valeurs

    def __repr__(self):
        return f"{self.nom}: {self.poids}"

    def __hash__(self) -> int:
        return hash(self.nom, self.poids)
