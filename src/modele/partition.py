from groupe import Groupe
from criteres.booleen import Booleen
from criteres.categorique import Categorique
from criteres.numerique import Numerique
class Partition:
    def __init__(self):
        self.groupes:set[Groupe] = set()

    def ajouter_groupe(self, groupe:Groupe) -> None:
        self.groupes.add(groupe)
    
    def get_groupes(self) -> set[Groupe]:
        return self.groupes
    
    def calcul_score(self) -> float:
        return sum(groupe.calcul_score() for groupe in self.groupes)
