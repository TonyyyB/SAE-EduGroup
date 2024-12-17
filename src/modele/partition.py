from groupe import Groupe
class Partition:
    def __init__(self):
        self.groupes:list[Groupe] = []

    def ajouter_groupe(self, groupe:Groupe) -> None:
        self.groupes.append(groupe)

    def get_groupes(self) -> set[Groupe]:
        return self.groupes

    def calcul_score(self) -> float:
        return sum(groupe.calcul_score() for groupe in self.groupes)
    
    def calcul_score_moyen(self) -> float:
        return sum(groupe.calcul_score() for groupe in self.groupes) / len(self.groupes) 
