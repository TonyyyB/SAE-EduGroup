class Eleve:
    def __init__(self, prenom, nom, num_etudiant, genre):
        self.prenom = prenom
        self.nom = nom
        self.num_etudiant = num_etudiant
        self.genre = genre
        self.criteres = {}  # Dictionnaire pour les matières et les critères
        self.score = 0  # Score calculé (moyenne pondérée)

    def ajouter_critere(self, critere, valeur):
        """Ajoute un critère avec une valeur associée au dictionnaire criteres."""
        self.criteres[critere] = valeur

    def calculer_moyenne_ponderee(self, coef_matieres):
        """Calcule la moyenne pondérée des critères (matières) selon les coefficients fournis."""
        total_coef = sum(coef_matieres[matiere] for matiere in self.criteres if matiere in coef_matieres)
        if total_coef == 0:
            return 0
        self.score = sum(self.criteres[matiere] * coef_matieres[matiere] for matiere in self.criteres if matiere in coef_matieres) / total_coef
        return self.score

    def __repr__(self):
        return f"{self.prenom} {self.nom} - Score: {self.score:.2f} - Genre: {self.genre}"
    
    def __hash__(self):
        return hash((self.num_etudiant, self.nom, self.prenom, self.genre))