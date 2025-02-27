from modele.eleve import Eleve
from modele.critere import Critere
class Groupe:
    def __init__(self, taille:int, criteres:set[Critere]=set()):
        self.taille:int = taille
        self.contraintes:dict[Critere,set[str]] = dict()  # Dictionnaire pour les contraintes
        self.eleves:set[Eleve] = set()
        self.criteres:set[Critere] = criteres
        self.aEteModifier = False
    
    def changer_taille(self, taille:int, enregistrer=True) -> None:
        if enregistrer:
            self.aEteModifier = True
        self.taille = taille
    
    def set_a_ete_modifier(self, aEteModifier) -> None:
        self.aEteModifier = aEteModifier
    
    def a_ete_modifier(self) -> bool:
        return self.aEteModifier
    
    def set_contrainte(self, critere:Critere, vals:set|list[int]) -> None:
        self.contraintes[critere] = set(vals)

    def respecter_contraintes(self, eleve:Eleve):
        for critere, valeurs in self.contraintes.items():
            if eleve.get_critere(critere) not in valeurs and len(valeurs) != 0:
                return False
        return True
    
    def calcul_prop(self) -> dict[Critere,dict[str,float]]:
        propActuel = dict()
        for critere in self.criteres:
            propActuel[critere] = dict()
            for valeur in critere.get_valeurs():
                propActuel[critere][valeur] = 0
            for eleve in self.get_eleves():
                propActuel[critere][eleve.get_critere(critere)] += 1
            for valeur in propActuel[critere]:
                propActuel[critere][valeur] /= self.get_taille()
        return propActuel
    
    def ajouter_eleve(self, eleve:Eleve) -> None:
        if len(self.eleves) + 1 > self.taille:
            return False
        self.eleves.add(eleve)
        if len(self.criteres) == 0:
            self.criteres = eleve.get_criteres().keys()
        return True

    def supp_eleve(self, eleve:Eleve) -> None:
        if eleve in self.eleves: self.eleves.remove(eleve)

    def place_dispo(self) -> bool:
        return len(self.eleves) + 1 <= self.taille

  def simule_ajout(self, groupe:Groupe, eleve:Eleve) -> float:
        if groupe not in self.groupes: return self.calcul_penalite()
        if eleve in groupe.get_eleves() or len(groupe.get_eleves()) + 1 > groupe.taille: return self.calcul_penalite()
        groupe.get_eleves().add(eleve)
        score = self.calcul_penalite()
        groupe.get_eleves().remove(eleve)
        return score

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

    def get_eleves(self) -> set[Eleve]:
        return self.eleves

    def set_criteres(self, criteres:list|set[Critere]) -> None:
        self.criteres = set(criteres)

    def get_contraintes(self) -> dict[Critere,set[int]]:
        return self.contraintes

    def get_contrainte(self, critere:Critere) -> set[int]:
        return self.contraintes[critere] if critere in self.contraintes else None

    def get_taille(self) -> int:
        return self.taille
    
    def clear(self) -> None:
        self.eleves.clear()

    def __repr__(self):
        return f"Groupe de {len(self.eleves)}"

    def __hash__(self):
        return hash((self.taille, frozenset(self.eleves), frozenset(self.criteres)))