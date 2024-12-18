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
        if eleve in groupe.get_eleves() or len(groupe.get_eleves()) + 1 > groupe.taille: return self.calcul_score()
        groupe.get_eleves().add(eleve)
        score = self.calcul_score()
        groupe.get_eleves().remove(eleve)
        return score

    def simule_supp(self, groupe:Groupe, eleve:Eleve) -> float:
        if groupe not in self.groupes: return self.calcul_score()
        if eleve not in groupe.get_eleves(): return self.calcul_score()
        groupe.get_eleves().remove(eleve)
        score = self.calcul_score()
        groupe.get_eleves().add(eleve)
        return score
    
    def simule_transf(self, groupe1:Groupe, groupe2:Groupe, eleve1:Eleve, eleve2:Eleve) -> tuple[float,float]: # type: ignore
        """Renvoie les deux score des deux groupes si un transfer est effectuer entre les deux élèves

        Args:
            groupe1 (Groupe): premier groupe
            groupe2 (Groupe): deuxième groupe
            eleve1 (Eleve): eleve du groupe
            eleve2 (Eleve): eleve de l'autre groupe

        Returns:
            float: score de la partition
        """
        if eleve1 not in groupe1.get_eleves() or eleve2 not in groupe2.get_eleves(): return self.calcul_score()
        groupe1.get_eleves().remove(eleve1)
        groupe2.get_eleves().remove(eleve2)
        groupe1.get_eleves().add(eleve2)
        groupe2.get_eleves().add(eleve1)
        scores = self.calcul_score()
        groupe1.get_eleves().remove(eleve2)
        groupe2.get_eleves().remove(eleve1)
        groupe1.get_eleves().add(eleve1)
        groupe2.get_eleves().add(eleve2)
        return scores

    def calcul_score(self) -> float:
        moyenne = sum(groupe.calcul_score() for groupe in self.groupes) / len(self.groupes)
        ecartType = 0
        for groupe in self.groupes:
            ecartType += (groupe.calcul_score() - moyenne) ** 2
        ecartType = math.sqrt(ecartType / len(self.groupes))
        return moyenne - ecartType
