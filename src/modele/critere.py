from groupe import Groupe
class Critere:
    def __init__(self, nom:str, poids:int):
        self.nom = nom
        self.poids = poids
        self.transpo = dict()

    def ajouter_valeur(self, valeur:int|bool|str, correspondance:int=None):
        if correspondance is None:
            if isinstance(valeur, int):
                correspondance = valeur
            elif isinstance(valeur, bool):
                correspondance = 1 if valeur else 0
            else:
                raise ValueError("La correspondance doit être renseignée pour le type str")
        self.transpo[valeur] = correspondance

    def set_poids(self, poids:int) -> None:
        self.poids = poids
    
    def get_poids(self) -> int:
        return self.poids
    
    def get_nom(self) -> str:
        return self.nom
    
    def to_int(self, val:int|bool|str) -> int:
        return self.transpo[val]
    
    def to_val(self, val:int) -> int|bool|str:
        for cle, valeur in self.transpo.items():
            if valeur == val:
                return cle
        return None
    def calcul_score(self, groupe:Groupe) -> float:
        pass
    