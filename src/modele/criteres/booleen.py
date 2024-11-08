from critere import Critere
from groupe import Groupe
class Booleen(Critere):
    def __init__(self, nom:str, poids:int):
        super().__init__(self, nom, poids)
    
    def calcul_score(self, groupe:Groupe) -> float:
        pass
