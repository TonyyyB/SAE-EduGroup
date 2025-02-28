from modele.groupe import Groupe
from modele.eleve import Eleve
from modele.critere import Critere
from tkinter import messagebox
import math
class Partition:
    def __init__(self, eleves:set[Eleve], criteres:set[Critere]):
        self.groupes:list[Groupe] = []
        self.eleves:set[Eleve] = eleves
        self.criteres:set[Critere] = criteres
        self.is_genere = False
        self.propGlobal:dict[Critere,dict[str,float]] = dict()
    
    def is_generer(self):
        return self.is_genere
    
    #def generer(self) -> 'Partition':
    #    self.clear()
    #    self.calcul_proportion()
    #    elevesAPlacer:set[Eleve] = set(self.eleves)
    #    groupes = self.get_groupes()
    #    # Initialisation
#
    #    # Groupes possibles
    #    for eleve in self.eleves:
    #        self.groupeEleve[eleve] = []
    #        for groupe in groupes:
    #            if groupe.respecter_contraintes(eleve):
    #                self.groupeEleve[eleve].append(groupe)
#
    #    # Ajout des élèves dans le seul groupe possible 
#
    #    for eleve,groupe in self.groupeEleve.items():
    #        if len(groupe) == 1:
    #            groupe[0].ajouter_eleve(eleve)
    #            elevesAPlacer.remove(eleve)
    #    
    #    # Ajout des autres élèves selon le score
    #    eleveNonPlacer = set()
    #    score = self.calcul_penalite()
    #    while (len(elevesAPlacer) > 0):
    #        eleve = elevesAPlacer.pop()
    #        groupes = self.groupeEleve[eleve]
    #        if len(self.groupeEleve[eleve]) == 0:
    #            eleveNonPlacer.add(eleve)
    #        else:
    #            groupeAAjouter = None
    #            for groupe in groupes:
    #                if self.simule_ajout(eleve, groupe) <= score:
    #                    groupeAAjouter = groupe
    #                    score = self.simule_ajout(eleve, groupe)
    #            if groupeAAjouter is not None:
    #                groupeAAjouter.ajouter_eleve(eleve)
    #            else:
    #                eleveNonPlacer.add(eleve)
    #    elevesAPlacer = eleveNonPlacer

    def generer(self) -> 'Partition':
        self.clear()
        self.calcul_proportion()
        # Calcul dico Eleve => groupes possibles
        groupesPossible:dict[Eleve, set[Groupe]] = dict()
        for eleve in self.eleves:
            groupesPossible[eleve] = set(groupe for groupe in self.groupes if groupe.respecter_contraintes(eleve))
        elevesRestants = list(groupesPossible.keys())
        # Ajout des élèves dans le seul groupe possible
        i = 0
        while i < len(elevesRestants):
            eleve = elevesRestants[i]
            groupes = groupesPossible[eleve]
            if len(groupes) == 1:
                groupes.pop().ajouter_eleve(eleve)
                elevesRestants.remove(eleve)
            else:
                i += 1
        # Ajouter les autres élèves
        i = 0
        while i < len(elevesRestants):
            eleve = elevesRestants[i]
            groupes = groupesPossible[eleve]
            gmax = None
            score = self.calcul_penalite()
            for groupe in groupes:
                score_groupe = self.simule_ajout(groupe, eleve)
                if (score_groupe < score or gmax is None) and (groupe.place_dispo()>0):
                    score = score_groupe
                    gmax = groupe

            if gmax is not None:
                gmax.ajouter_eleve(eleve)
                elevesRestants.remove(eleve)
            else:
                i += 1
        self.eleves_restant = elevesRestants
        self.is_genere = True
        return self
    
    def simule_ajout(self, groupe:Groupe, eleve:Eleve) -> float:
        if groupe not in self.groupes: return self.calcul_penalite()
        if eleve in groupe.get_eleves() or len(groupe.get_eleves()) + 1 > groupe.taille: return self.calcul_penalite()
        groupe.get_eleves().add(eleve)
        score = self.calcul_penalite()
        groupe.get_eleves().remove(eleve)
        return score
    
    def get_eleves_restant(self):
        if self.is_genere:
            return self.eleves_restant
        else:
            return self.eleves

    def simule_supp(self, groupe:Groupe, eleve:Eleve) -> float:
        if groupe not in self.groupes: return self.calcul_penalite()
        if eleve not in groupe.get_eleves(): return self.calcul_penalite()
        groupe.get_eleves().remove(eleve)
        score = self.calcul_penalite()
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
        if eleve1 not in groupe1.get_eleves() or eleve2 not in groupe2.get_eleves(): return self.calcul_penalite()
        groupe1.get_eleves().remove(eleve1)
        groupe2.get_eleves().remove(eleve2)
        groupe1.get_eleves().add(eleve2)
        groupe2.get_eleves().add(eleve1)
        scores = self.calcul_penalite()
        groupe1.get_eleves().remove(eleve2)
        groupe2.get_eleves().remove(eleve1)
        groupe1.get_eleves().add(eleve1)
        groupe2.get_eleves().add(eleve2)
        return scores
    
    def calcul_penalite(self) -> float:
        penalite = 0
        propsGroupes:dict[Groupe,dict[Critere,dict[str,float]]] = dict()
        for groupe in self.groupes:
            propsGroupes[groupe] = groupe.calcul_prop()

        for critere in self.criteres:
            penaliteCritere = 0
            for groupe in self.groupes:
                if critere not in propsGroupes[groupe]:
                    continue
                for valeur in critere.get_valeurs():
                    penaliteCritere += abs(propsGroupes[groupe][critere][valeur] - self.propGlobal[critere][valeur])
            penalite += critere.get_poids() + penaliteCritere
        return penalite

    def calcul_proportion(self) -> dict[Critere,dict[str,float]]:
        self.propGlobal = dict()
        for critere in self.criteres:
            self.propGlobal[critere] = dict()
            for valeur in critere.get_valeurs():
                self.propGlobal[critere][valeur] = 0
            for eleve in self.eleves:
                self.propGlobal[critere][eleve.get_critere(critere)] += 1
            for valeur in self.propGlobal[critere]:
                self.propGlobal[critere][valeur] /= len(self.eleves)
        return self.propGlobal

    def adapter_taille(self) -> None:
        groupesTailleModif, groupesSansTailleModif = self.groupes_avec_et_sans_taille_modif()

        # S'il n'y a pas de groupes sans taille modifiée, on ne fait rien
        if len(groupesSansTailleModif) == 0:
            return

        # Calcul du nombre d'élèves restants après avoir pris en compte les groupes modifiés
        nbElevesRestants = len(self.eleves) - sum(groupe.get_taille() for groupe in groupesTailleModif)

        # Si le nombre d'élèves restants est négatif, il y a un problème de dépassement
        if nbElevesRestants < 0:
            raise ValueError("La somme des tailles des groupes dépasse le nombre total d'élèves.")

        # Répartir les élèves restants dans les groupes non modifiés
        nbParGroupe = nbElevesRestants // len(groupesSansTailleModif)
        surplus = nbElevesRestants % len(groupesSansTailleModif)  # Pour répartir les restes

        for i, groupe in enumerate(groupesSansTailleModif):
            nouvelle_taille = nbParGroupe + (1 if i < surplus else 0)  # Ajouter un élève aux 'surplus' premiers groupes
            groupe.changer_taille(nouvelle_taille, enregistrer=False)  # Utiliser 'enregistrer=False' ici pour ne pas marquer la modification

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
    
    def clear(self) -> None:
        for groupe in self.groupes:
            groupe.clear()
        self.is_genere = False