from modele.eleve import Eleve
from modele.critere import Critere
class Groupe:
    def __init__(self, taille:int, contraintes:set[Critere]=dict()):
        self.taille:int = taille
        self.contraintes:dict[Critere,set[str]] = contraintes  # Dictionnaire pour les contraintes
        self.eleves:set[Eleve] = set()
        self.criteres:set[Critere] = set()
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
    
    def calcul_score(self) -> float:
        if len(self.eleves) == 0: return 0.0
        return sum(critere.calcul_score(self) for critere in self.criteres)
    
    def clear(self) -> None:
        self.eleves.clear()

    def __repr__(self):
        return f"Groupe de {len(self.eleves)} score de {self.calcul_score()}"

    def __hash__(self):
        return hash((self.taille, frozenset(self.eleves), frozenset(self.criteres)))