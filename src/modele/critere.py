from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from groupe import Groupe
class Critere:
    def __init__(self, nom:str, poids:int, repartition:bool):
        self.nom:str = nom
        self.poids:int = poids
        self.repartition:bool = repartition
        self.transpo:dict[int|bool|str,int] = dict()

    def ajouter_valeur(self, valeur:int|bool|str, correspondance:int=None) -> None:
        if valeur not in self.transpo.keys():
            if correspondance is None:
                if isinstance(valeur, int):
                    correspondance = valeur
                elif isinstance(valeur, bool):
                    correspondance = 1 if valeur else 0
                else:
                    if len(valeur) == 1:
                        correspondance = ord(valeur) - ord('A') + 1
                    else:
                        correspondance = len(self.transpo.keys())+1
                    print(f"Valeur ajoutée: {valeur} -> {correspondance}")
            self.transpo[valeur] = correspondance

    def set_poids(self, poids:int) -> None:
        self.poids:int = poids
    def get_poids(self) -> int:
        return self.poids
    
    def set_repratis(self, repartis:bool) -> None:
        self.repartition:bool = repartis

    def get_nom(self) -> str:
        return self.nom
    def est_reparti(self) -> bool:
        return self.repartition

    def to_int(self, val:int|bool|str) -> int:
        return self.transpo[val]

    def to_val(self, val:int) -> int|bool|str:
        for cle, valeur in self.transpo.items():
            if valeur == val:
                return cle
        return None

    def calcul_score(self, groupe:'Groupe') -> float:
        pass

    def get_transpo(self) -> dict[int|bool|str,int]:
        return self.transpo
    
    def get_valeurs_possibles(self, toVal=False) -> set[int]|set[int|bool|str]:
        return set(self.transpo.keys()) if toVal else set(self.transpo.values())

    def __repr__(self):
        return f"{self.nom}: {self.poids}"

    def __hash__(self) -> int:
        return hash(self.nom)
