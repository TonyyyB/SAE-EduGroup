from critere import Critere
from groupe import Groupe
class Numerique(Critere):
    def __init__(self, nom:str, poids:int):
        super().__init__(self, nom, poids)

    def calcul_score(self, groupe:Groupe) -> float:
        valeurs = [eleve.get_critere(self) for eleve in groupe.get_eleves()]
        if self.est_reparti():
            moyenne = sum(valeurs) / len(valeurs)
            variance = sum((x - moyenne) ** 2 for x in valeurs) / len(valeurs)
            score = variance
        else:
            # Proximité (1 - écart moyen)
            differences = sum(abs(x - y) for x in valeurs for y in valeurs if x != y)
            max_diff = 5 * len(valeurs) * (len(valeurs) - 1)
            score = 1 - differences / max_diff if max_diff != 0 else 1
        return score * self.poids