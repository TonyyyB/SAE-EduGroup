from modele.critere import Critere
from modele.groupe import Groupe
class Categorique(Critere):
    def __init__(self, nom:str, poids:int):
        super().__init__(self, nom, poids)
    
    def calcul_score(self, groupe:Groupe) -> float:
        pass
        