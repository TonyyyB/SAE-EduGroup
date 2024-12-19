from modele.groupe import Groupe
from modele.eleve import Eleve
import math
class Partition:
    def __init__(self):
        self.groupes:list[Groupe] = []
        self.is_genere = False
    
    def is_generer(self):
        return self.is_genere
    
    def generer(self, eleves:list|set[Eleve]) -> 'Partition':
        self.clear()
        elevesAPlacer:set[Eleve] = set(eleves)
        groupes = self.get_groupes()
        # Initialisation
        for eleve in eleves:
            maxi = -math.inf
            gmax = None
            for groupe in groupes:
                if not groupe.respecter_contraintes(eleve) or not groupe.place_dispo(): continue
                score = self.simule_ajout(groupe, eleve)
                if score > maxi:
                    maxi = score
                    gmax = groupe
            if gmax is not None:
                gmax.ajouter_eleve(eleve)
                elevesAPlacer.remove(eleve)
        while len(elevesAPlacer) > 0:
            eleve = elevesAPlacer.pop()
            maxi = -math.inf
            gmax = None
            for groupe in groupes:
                if not groupe.place_dispo(): continue
                score = self.simule_ajout(groupe,eleve)
                if score > maxi:
                    maxi = score
                    gmax = groupe
            gmax.ajouter_eleve(eleve)
        # Boucle principale
        combinaisons:set[tuple[Groupe,Groupe]] = set()
        for groupe1 in groupes:
            for groupe2 in groupes:
                if groupe1 == groupe2: continue
                if (groupe2, groupe1) not in combinaisons:
                    combinaisons.add((groupe1, groupe2))

        lastScore = self.calcul_score()
        newScore = lastScore + 1
        timeLastScoreNotGreater = 0
        while(timeLastScoreNotGreater < 3):
            lastScore = newScore
            for g1, g2 in combinaisons:
                newScore = self.calcul_score()
                maxiEvol = 0
                evolMax = None
                maxiEvolSansContraintes = 0
                evolMaxSansContraintes = None
                for e1, e2 in zip(g1.get_eleves(), g2.get_eleves()):
                    score = self.simule_transf(g1, g2, e1, e2)
                    if not g1.respecter_contraintes(e2) or not g2.respecter_contraintes(e1):
                        if score > maxiEvolSansContraintes:
                            maxiEvolSansContraintes = score
                            evolMaxSansContraintes = (g1, g2, e1, e2)
                    else:
                        if score > maxiEvol:
                            maxiEvol = score
                            evolMax = (g1, g2, e1, e2)
                if evolMax is None:
                    if evolMaxSansContraintes is not None:
                        evolMaxSansContraintes[0].transferer(evolMaxSansContraintes[1], 
                                                            evolMaxSansContraintes[2], 
                                                            evolMaxSansContraintes[3])
                else:
                    evolMax[0].transferer(evolMax[1], evolMax[2], evolMax[3])
            newScore = self.calcul_score()
            if newScore > lastScore:
                timeLastScoreNotGreater = 0
            else:
                timeLastScoreNotGreater += 1
        self.is_genere = True
        return self

    def ajouter_groupe(self, groupe:Groupe) -> None:
        self.groupes.append(groupe)
    
    def supprimer_groupe(self, groupe:Groupe) -> None:
        if groupe in self.groupes: self.groupes.remove(groupe)

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
        ecart_type = 0
        for groupe in self.groupes:
            ecart_type += (groupe.calcul_score() - moyenne) ** 2
        ecart_type = math.sqrt(ecart_type / len(self.groupes))
        return moyenne - ecart_type
    
    def clear(self) -> None:
        for groupe in self.groupes:
            groupe.clear()
        self.is_genere = False
