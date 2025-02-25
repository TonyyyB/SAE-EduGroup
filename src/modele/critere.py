from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from groupe import Groupe
class Critere:
    def __init__(self, nom:str, poids:int, valPossible:set):
        self.nom:str = nom
        self.poids:int = poids
        self.valPossible: set = valPossible
        self.proportionGlobale: dict = None
        

    def set_poids(self, poids:int) -> None:
        self.poids:int = poids
    def get_poids(self) -> int:
        return self.poids

    def get_nom(self) -> str:
        return self.nom
    
    def get_proportionGlobale(self,valeur) -> float:
        return self.proportionGlobale[valeur]
    
    def calcul_proportion(self, eleves):
        nb = 0
        dico = dict()
        for valeur in self.valPossible:
            for eleve in eleves:
                if eleve.get_critere(self) == valeur:
                    nb += 1
            dico[valeur] = nb / len(eleves)
        self.proportionGlobale = dico

    
    def get_valPossible(self) -> set:
        return self.valPossible




    def calcul_score(self, groupes:['Groupe']) -> float:
        somme = 0
        for groupe in groupes:
            for val in self.valPossible:
                somme += groupe.calcul_score(self,val)
        return somme * self.get_poids()

    
    def get_valeurs_possibles(self, toVal=False) -> set[int]|set[int|bool|str]:
        return self.valPossible

    def __repr__(self):
        return f"{self.nom}: {self.poids}"

    def __hash__(self) -> int:
        return hash(self.nom)
