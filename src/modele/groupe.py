from modele.eleve import Eleve
from modele.critere import Critere
class Groupe:
    def __init__(self, taille:int, contraintes:set[Critere]=dict()):
        self.taille:int = taille
        self.contraintes:dict[Critere,set[int]] = contraintes  # Dictionnaire pour les contraintes
        self.eleves:set[Eleve] = set()
        self.criteres:set[Critere] = set()

    def ajouter_contrainte(self, critere:Critere, vals:set|list[int]) -> None:
        self.contraintes[critere] = set(vals)
    
    def ajouter_eleve(self, eleve:Eleve) -> None:
        if self.taille + 1 >= self.taille:
            return False
        self.eleves.add(eleve)
        if len(self.criteres) == 0:
            self.criteres = eleve.get_criteres().keys()
        return True
    
    def get_eleves(self) -> set[Eleve]:
        return self.eleves
    
    def set_criteres(self, criteres:list|set[Critere]) -> None:
        self.criteres = set(criteres)
    
    def get_contraintes(self) -> dict[Critere,set[int]]:
        return self.contraintes
    
    def get_contrainte(self, critere:Critere) -> set[int]:
        return self.contraintes[critere] if critere in self.contraintes else None
    
    def calcul_score(self) -> float:
        return sum(critere.calcul_score(self) for critere in self.criteres)
    