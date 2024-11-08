from eleve import Eleve
from groupe import Groupe
from partition import Partition
from critere import Critere

def algo(eleves, nb_groupes, tailles, contraintes, coef_matieres):
    # Initialiser la partition de groupes
    partition = Partition()
    
    # Création des groupes en respectant les tailles et en ajoutant les contraintes
    groupes = []
    for i in range(nb_groupes):
        groupe = Groupe(tailles[i])
        if i in contraintes:
            for critere, valeurs in contraintes[i].items():
                groupe.ajouter_contrainte(critere, valeurs)
        groupes.append(groupe)
    
    # Calcul de la moyenne pondérée des scores pour chaque élève
    for eleve in eleves:
        eleve.score = eleve.calculer_moyenne_ponderee(coef_matieres)

    # Trier les élèves par score pour équilibrer les groupes en termes de niveau
    eleves.sort(key=lambda x: x.score, reverse=True)
    
    # Répartir les élèves en fonction des contraintes et tailles des groupes
    for eleve in eleves:
        placed = False
        for groupe in groupes:
            if len(groupe.eleves) < groupe.taille and respecter_contraintes(groupe, eleve):
                groupe.ajouter_eleve(eleve)
                placed = True
                break
        if not placed:
            print(f"Impossible de placer {eleve.prenom} {eleve.nom} dans un groupe avec les contraintes actuelles.")
    
    # Ajouter chaque groupe à la partition finale
    for groupe in groupes:
        partition.ajouter_groupe(groupe)
    
    return partition

def respecter_contraintes(groupe, eleve):
    """Vérifie si un élève respecte les contraintes d'un groupe."""
    for critere, valeurs in groupe.contraintes.items():
        if critere in eleve.criteres and eleve.criteres[critere] not in valeurs:
            return False
    return True

def afficher_partition(partition):
    """Affiche la répartition des élèves dans chaque groupe."""
    for i, groupe in enumerate(partition.groupes):
        print(f"Groupe {i+1} (Taille: {len(groupe.eleves)} / {groupe.taille}):")
        for eleve in groupe.get_eleves():
            print(f"  - {eleve}")
        print()

# Exemple d'utilisation
donnees_eleves = [
    (3, "Leclerc", "Paul", "M", 2, 5, "A"),
    (4, "Lemoine", "Claire", "F", 3, 2, "B"),
    (5, "Bernard", "Marc", "M", 4, 1, "A"),
    (6, "Durand", "Isabelle", "F", 5, 3, "C"),
    (7, "Chauvin", "Luc", "M", 6, 5, "C"),
    (8, "Girard", "Caroline", "F", 3, 4, "A"),
    (9, "Robert", "Jacques", "M", 1, 1, "C"),
    (10, "Thibault", "Martine", "F", 1, 3, "B"),
    (11, "Faure", "David", "M", 2, 2, "B"),
    (12, "Legrand", "Elise", "F", 4, 2, "A"),
    (13, "Pierre", "Michel", "M", 6, 2, "C"),
    (14, "Moreau", "Lucie", "F", 5, 3, "A"),
    (15, "Guillot", "Henri", "M", 3, 2, "B"),
    (16, "Meunier", "Emilie", "F", 1, 5, "C"),
    (17, "Chevalier", "Alain", "M", 2, 5, "C"),
    (18, "Veron", "Denise", "F", 4, 3, "B"),
    (19, "Paillard", "Jacques", "M", 5, 2, "A"),
    (20, "Lemoine", "Philippe", "M", 6, 4, "A")
]

# Créer la liste des objets `Eleve`
eleves = []
for data in donnees_eleves:
    num_etudiant, nom, prenom, genre, francais, maths, penebilite = data
    eleve = Eleve(prenom, nom, num_etudiant, genre)
    eleve.ajouter_critere("Français", francais)
    eleve.ajouter_critere("Maths", maths)
    penebilite_score = {"A": 1, "B": 2, "C": 3}.get(penebilite, 0)
    eleve.ajouter_critere("Pénébilite", penebilite_score)
    eleves.append(eleve)

# Coefficients de pondération pour chaque matière
coef_matieres = {'Français': 0, 'Maths': 2, 'Pénébilite': 1}

# Appel de l'algorithme avec 3 groupes et des contraintes par genre 
partition = algo(
    eleves=eleves,
    nb_groupes=3,
    tailles=[8, 6, 6],
    contraintes={
        0: {'genre': ['F']},
        1: {'genre': ['M']}
    },
    coef_matieres=coef_matieres
)

# Afficher la répartition finale des groupes
afficher_partition(partition)
