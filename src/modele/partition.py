from groupe import Groupe
from criteres.booleen import Booleen
from criteres.categorique import Categorique
from criteres.numerique import Numerique
class Partition:
    def __init__(self):
        self.groupes:list[Groupe] = []

    def ajouter_groupe(self, groupe:Groupe) -> None:
        self.groupes.append(groupe)
    
    def calcul_score(self) -> float:
        total_score_groupes = sum(groupe.calcul_score() for groupe in self.groupes)

        # Calcul de la pénalité de progression sur tous les critères
        penalite_progression = 0
        for critere in self.criteres:
            valeurs_groupe_prec = [eleve.get_critere(critere) for eleve in self.groupes[0].get_eleves()]
            moyenne_groupe_prec = sum(valeurs_groupe_prec) / len(valeurs_groupe_prec)
            # Pour chaque critère, vérifier la progression entre les groupes
            for i in range(1,len(self.groupes)):
                # Calcul de la moyenne du critère dans le groupe actuel et le groupe suivant
                valeurs_groupe_i = [eleve.get_critere(critere) for eleve in self.groupes[i].get_eleves()]
                moyenne_groupe_i = sum(valeurs_groupe_i) / len(valeurs_groupe_i)
                
                # Calcul de la pénalité en fonction de l'ordre souhaité
                if isinstance(critere, Numerique):
                    # Pour les critères numériques, on s'assure d'une progression (ex. du plus fort au plus faible)
                    penalite_progression += critere.get_poids() * max(0, moyenne_groupe_prec - moyenne_groupe_i)
                elif isinstance(critere, Booleen) or isinstance(critere, Categorique):
                    # Pour les booléens et catégoriques, on peut également appliquer une logique de progression
                    # Ici, on prend une différence absolue entre les moyennes pour pénaliser les écarts
                    penalite_progression += critere.get_poids() * abs(moyenne_groupe_prec - moyenne_groupe_i)
                valeurs_groupe_prec = valeurs_groupe_i
                moyenne_groupe_prec = moyenne_groupe_i

        # Poids de la pénalité de progression
        lambda_coef = 10  # Ajuster ce coefficient selon l'importance de la progression
        total_score = total_score_groupes - lambda_coef * penalite_progression

        return total_score