from modele.critere import Critere
from modele.groupe import Groupe
class Booleen(Critere):
    def __init__(self, nom:str, poids:int):
        super().__init__(self, nom, poids)
    
    def calcul_score(self, groupe:Groupe) -> float:
        valeurs = [eleve.get_critere(self) for eleve in groupe.get_eleves()]
        count_vrai = valeurs.count(True)
        count_faux = len(valeurs) - count_vrai

        if self.est_reparti():
            ideal = len(valeurs) / 2
            score = 1 - abs(ideal - count_vrai) / len(valeurs)
        else:
            score = (count_vrai * (count_vrai - 1) + count_faux * (count_faux - 1)) / (len(valeurs) * (len(valeurs) - 1))
        
        return score * self.poids
