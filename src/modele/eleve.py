from modele.critere import Critere
class Eleve:
    def __init__(self, prenom:str, nom:str, num_etudiant:int, genre:bool):
        self.prenom:str = prenom
        self.nom:str = nom
        self.num_etudiant:int = num_etudiant
        self.genre:bool = genre
        self.criteres:dict[Critere,int|str] = {}  # Dictionnaire pour les matières et les critères
        self.groupes_possible = set()

    def ajouter_critere(self, critere:Critere, valeur:int|str):
        """Ajoute un critère avec une valeur associée au dictionnaire criteres."""
        self.criteres[critere] = valeur

    def ajouter_groupes_possible(self, groupe):
        self.groupes_possible.add(groupe)
    def get_groupes_possible(self):
        return self.groupes_possible
    
    def get_id(self):
        return self.num_etudiant
    def get_nom(self):
        return self.nom

    def get_prenom(self):
        return self.prenom

    def get_genre(self):
        return self.genre

    def get_criteres(self):
        return self.criteres

    def get_critere(self, critere):
        return self.criteres[critere]

    def __eq__(self, other):
        return isinstance(other, Eleve) and self.num_etudiant == other.num_etudiant

    def __repr__(self):
        return f"{self.prenom} {self.nom} - Genre: {self.genre}, {[c.get_nom() + ":" + str(self.criteres[c]) for c in self.criteres]}"

    def __hash__(self):
        return hash((self.num_etudiant, self.nom, self.prenom, self.genre))
