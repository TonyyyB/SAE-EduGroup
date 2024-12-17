from critere import Critere
from groupe import Groupe
class Categorique(Critere):
    def __init__(self, nom:str, poids:int, repartition:bool):
        super().__init__(nom, poids, repartition)
    
    def calcul_score(self, groupe:Groupe) -> float:
        valeurs = [eleve.get_critere(self) for eleve in groupe.get_eleves()]
        categories = set(valeurs)
        
        if self.est_reparti:
            ideal_count = len(valeurs) / len(categories)
            score = 1 - sum(abs(ideal_count - valeurs.count(cat)) for cat in categories) / len(valeurs)
        else:
            score = sum(valeurs.count(cat) * (valeurs.count(cat) - 1) for cat in categories) / (len(valeurs) * (len(valeurs) - 1))

        return score * self.poids
        