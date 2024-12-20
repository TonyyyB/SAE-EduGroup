from modele.groupe import Groupe
from modele.eleve import Eleve
from modele.critere import Critere
import math
class Partition:
    def __init__(self, eleves:set[Eleve]):
        self.groupes:list[Groupe] = []
        self.eleves:set[Eleve] = eleves
        self.criteres:set[Critere] = set() if len(eleves) == 0 else set(next(iter(eleves)).get_criteres().keys())
        self.is_genere = False
    
    def is_generer(self):
        return self.is_genere
    
    def generer(self) -> 'Partition':
        self.clear()
        elevesAPlacer:set[Eleve] = set(self.eleves)
        groupes = self.get_groupes()
        # Initialisation
        for eleve in self.eleves:
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
    
    def adapter_taille(self) -> None:
        groupesTailleModif, groupesSansTailleModif = self.groupes_avec_et_sans_taille_modif()
        if len(groupesSansTailleModif) == 0: return
        nbElevesRestants = len(self.eleves) - sum([groupe.get_taille() for groupe in groupesTailleModif])
        nbParGroupe = nbElevesRestants // len(groupesSansTailleModif)
        for groupe in self.groupes:
            groupe.changer_taille(nbParGroupe, False)
            nbElevesRestants -= nbParGroupe
        for i in range(nbElevesRestants):
            self.groupes[i].changer_taille(self.groupes[i].get_taille()+1, False)
        print()

    def groupes_avec_et_sans_taille_modif(self) -> tuple[list[Groupe], list[Groupe]]:
        tailleModif = []
        tailleNonModif = []
        for groupe in self.groupes:
            if groupe.a_ete_modifier(): tailleModif.append(groupe)
            else: tailleNonModif.append(groupe)
        return tailleModif, tailleNonModif
    
    def get_eleves_pas_possible_a_placer(self):
        return len(self.eleves) - sum([groupe.get_taille() for groupe in self.groupes])
    
    def ajouter_groupe(self, groupe:Groupe) -> None:
        self.clear()
        self.groupes.append(groupe)
    
    def supprimer_groupe(self, groupe_or_index:Groupe|int) -> None:
        if isinstance(groupe_or_index, Groupe):
            if groupe_or_index in self.groupes: 
                self.clear()
                self.groupes.remove(groupe_or_index)
        else:
            if groupe_or_index < 0 or groupe_or_index >= len(self.groupes): return
            self.clear()
            del self.groupes[groupe_or_index]

    def get_groupes(self) -> set[Groupe]:
        return self.groupes
    
    def get_criteres(self) -> set[Critere]:
        return self.criteres

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
