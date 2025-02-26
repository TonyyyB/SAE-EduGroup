from modele.groupe import Groupe
from modele.eleve import Eleve
from modele.critere import Critere
from tkinter import messagebox
import math
class Partition:
    def __init__(self, eleves:set[Eleve]):
        self.groupes:list[Groupe] = []
        self.eleves:set[Eleve] = eleves
        self.criteres:set[Critere] = set() if len(eleves) == 0 else set(next(iter(eleves)).get_criteres().keys())
        self.is_genere = False
        self.groupeEleve = dict()
    
    def is_generer(self):
        return self.is_genere
    
    def generer(self) -> 'Partition':
        self.clear()
        return self
        elevesAPlacer:set[Eleve] = set(self.eleves)
        groupes = self.get_groupes()
        # Initialisation

        # Groupes possibles
        for eleve in self.eleves:
            self.groupeEleve[eleve] = []
            for groupe in groupes:
                if groupe.respecter_contraintes(eleve):
                    self.groupeEleve[eleve].append(groupe)
            


        # Ajout des élèves dans le seul groupe possible 

        for eleve,groupe in self.eleves.items():
            if len(groupe) == 1:
                groupe[0].ajouter_eleve(eleve)
                elevesAPlacer.remove(eleve)
        
        # Ajout des autres élèves selon le score
        eleveNonPlacer = set()
        score = self.calcul_score()
        while (elevesAPlacer > 0):
            eleve = elevesAPlacer.pop()
            groupes = self.eleves[eleve]
            if len(self.groupeEleve[eleve]) == 0:
                eleveNonPlacer.add(eleve)
            else:
                groupeAAjouter = None
                for groupe in groupes:
                    if self.simule_ajout(eleve, groupe) <= score:
                        groupeAAjouter = groupe
                        score = self.simule_ajout(eleve, groupe)
                if groupeAAjouter is not None:
                    groupeAAjouter.ajouter_eleve(eleve)
                else:
                    eleveNonPlacer.add(eleve)
        elevesAPlacer = eleveNonPlacer
       
    
    def calcul_penalite(self) -> float:
        penalite = 0
    
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
