from groupe import Groupe
from eleve import Eleve
import math
class Partition:
    def __init__(self):
        self.groupes:list[Groupe] = []

    def ajouter_groupe(self, groupe:Groupe) -> None:
        self.groupes.append(groupe)

    def get_groupes(self) -> set[Groupe]:
        return self.groupes
    
    def simule_ajout(self, groupe:Groupe, eleve:Eleve) -> float:
        if groupe not in self.groupes: return self.calcul_score()
        if eleve in groupe.eleves or len(groupe.eleves) + 1 > groupe.taille: return self.calcul_score()
        groupe.eleves.add(eleve)
        score = self.calcul_score()
        groupe.eleves.remove(eleve)
        return score

    def simule_supp(self, groupe:Groupe, eleve:Eleve) -> float:
        if groupe not in self.groupes: return self.calcul_score()
        if eleve not in groupe.eleves: return self.calcul_score()
        groupe.eleves.remove(eleve)
        score = self.calcul_score()
        groupe.eleves.add(eleve)
        return score

    def calcul_score(self) -> float:
        moyenne = sum(groupe.calcul_score() for groupe in self.groupes) / len(self.groupes)
        ecartType = 0
        for groupe in self.groupes:
            ecartType += (groupe.calcul_score() - moyenne) ** 2
        return moyenne - math.sqrt(ecartType/len(self.groupes))
