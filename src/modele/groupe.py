from modele.eleve import Eleve
from modele.critere import Critere
class Groupe:
    def __init__(self, taille:int, contraintes:set[Critere]=None):
        self.taille:int = taille
        if contraintes is None:
            self.contraintes:dict[Critere,set[int]] = dict()
        else:
            self.contraintes:dict[Critere,set[int]] = contraintes  # Dictionnaire pour les contraintes
        self.eleves:set[Eleve] = set()
        self.criteres:set[Critere] = set()
        self.aEteModifier = False
    
    def changer_taille(self, taille:int, enregistrer=True) -> None:
        if enregistrer:
            self.aEteModifier = True
        self.taille = taille
    
    def a_ete_modifier(self) -> bool:
        return self.aEteModifier
    
    def set_contrainte(self, critere:Critere, vals:set|list[int]) -> None:
        self.contraintes[critere] = set(vals)

    def respecter_contraintes(self, eleve:Eleve):
        """Vérifie si un élève respecte les contraintes d'un groupe."""
        for critere, valeurs in self.contraintes.items():
            if eleve.get_critere(critere) not in valeurs:
                return False
        return True
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

    def simule_ajout(self, eleve:Eleve) -> float:
        if eleve in self.eleves or len(self.eleves) + 1 > self.taille: return self.calcul_score()
        self.eleves.add(eleve)
        score = self.calcul_score()
        self.eleves.remove(eleve)
        return score

    def simule_supp(self, eleve:Eleve) -> float:
        if eleve not in self.eleves: return self.calcul_score()
        self.eleves.remove(eleve)
        score = self.calcul_score()
        self.eleves.add(eleve)
        return score

    def simule_transf(self, groupe:'Groupe', eleve1:Eleve, eleve2:Eleve) -> tuple[float,float]: # type: ignore
        """Renvoie les deux score des deux groupes si un transfer est effectuer entre les deux élèves

        Args:
            groupe (Groupe): groupe concerné
            eleve1 (Eleve): eleve du groupe
            eleve2 (Eleve): eleve de l'autre groupe

        Returns:
            (float,float): score du groupe, score de l'autre groupe
        """
        if eleve1 not in self.eleves or eleve2 not in groupe.get_eleves(): return self.calcul_score(), groupe.calcul_score()
        self.eleves.remove(eleve1)
        groupe.get_eleves().remove(eleve2)
        self.eleves.add(eleve2)
        groupe.get_eleves().add(eleve1)
        scores = self.calcul_score(), groupe.calcul_score()
        self.eleves.remove(eleve2)
        groupe.get_eleves().remove(eleve1)
        self.eleves.add(eleve1)
        groupe.get_eleves().add(eleve2)
        return scores

    def transferer(self, groupe:'Groupe', eleve1:Eleve, eleve2:Eleve):
        if eleve1 not in self.eleves or eleve2 not in groupe.get_eleves(): return self.calcul_score(), groupe.calcul_score()
        self.eleves.remove(eleve1)
        groupe.get_eleves().remove(eleve2)
        self.eleves.add(eleve2)
        groupe.get_eleves().add(eleve1)

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
    
    def calcul_score(self,critere,valCritere) -> float:
        if len(self.eleves) == 0: return 0.0
        proportion = 0
        for eleve in self.eleves:
            if eleve.get_critere(critere)[valCritere]:
                proportion += 1
        proportion /= len(self.eleves)
        return abs(proportion-critere.get_proportionGlobale())
    
    def clear(self) -> None:
        self.eleves.clear()

    def __repr__(self):
        return f"Groupe de {len(self.eleves)} score de {self.calcul_score()}"

    def __hash__(self):
        return hash((self.taille, frozenset(self.eleves), frozenset(self.criteres)))