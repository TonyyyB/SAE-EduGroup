from eleve import Eleve
from groupe import Groupe
from partition import Partition
from critere import Critere
from criteres.booleen import Booleen
from criteres.categorique import Categorique
from criteres.numerique import Numerique
import math

def algo(eleves:list|set[Eleve], partition:Partition):
    elevesAPlacer:set[Groupe] = set()
    groupes = partition.get_groupes()
    # Initialisation 
    for groupe in groupes:
        for eleve in eleves:
            peutEtrePlacer = True
            for critere in eleve.get_criteres():
                contrainte = groupe.get_contrainte(critere)
                if contrainte is None: continue
                if eleve.get_critere(critere) not in contrainte:
                    peutEtrePlacer = False
            if peutEtrePlacer:
                groupe.ajouter_eleve(eleve)
            else:
                elevesAPlacer.add(eleve)
    for eleve in elevesAPlacer:
        maxi = 0
        gmax = None
        for groupe in groupes:
            score = groupe.simule_ajout(eleve)
            if score > maxi:
                maxi = score
                gmax = groupe
        if gmax is None:
            print("Erreur")
        else:
            gmax.ajouter_eleve(eleve)
    
    # Boucle principale
    lastScore = 0
    newScore = 1
    while(newScore > lastScore):
        lastScore = newScore
        a_transferer = dict()
        for groupe in groupes:
            a_transferer[groupe] = get_mieux_a_retirer(groupe)
        to_test:set[Groupe] = set(a_transferer.keys())
        transfert = (0, None)
        while len(to_test) > 0:
            groupe = to_test.pop()
            if a_transferer[groupe] is None: continue
            maxi = (0,0)
            tmax = None
            for g in to_test:
                if a_transferer[g] is None: continue
                score = groupe.simule_transf(g, a_transferer[groupe], a_transferer[g])
                if sum(score) > sum(maxi):
                    maxi = score
                    tmax = {groupe:a_transferer[groupe], g:a_transferer[g]}
            if tmax is None: continue
            if sum(maxi) > transfert[0]:
                transfert = sum(maxi), tmax
        if transfert[1] is not None:
            g1, g2 = transfert[1].keys()
            g1.transferer(g2, transfert[1][g1], transfert[1][g2])
        newScore = partition.calcul_score()
    return partition


def get_mieux_a_retirer(groupe:Groupe):
    """Renvoie l'élève qui, si il est retirer, permet de monter le score du groupe

    Args:
        groupe (Groupe): groupe

    Returns:
        Eleve: élève, None si aucun ne fait descendre le score
    """
    maxi = 0
    emax = None
    for eleve in groupe.get_eleves():
        score = groupe.simule_supp(eleve)
        if score > maxi:
            maxi = score
            emax = eleve
    return emax

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
critereFrancais = Numerique("Français",10, True)
critereMath = Numerique("Maths",5, True)
criterePenibilite = Numerique("Pénibilité", 3, True)
# Créer la liste des objets `Eleve`
eleves = []
for data in donnees_eleves:
    num_etudiant, nom, prenom, genre, francais, maths, penebilite = data
    eleve = Eleve(prenom, nom, num_etudiant, genre)
    eleve.ajouter_critere(critereFrancais, francais)
    eleve.ajouter_critere(critereMath, maths)
    penebilite_score = {"A": 1, "B": 2, "C": 3}.get(penebilite, 0)
    eleve.ajouter_critere(criterePenibilite, penebilite_score)
    eleves.append(eleve)

# Coefficients de pondération pour chaque matière
coef_matieres = {'Français': 0, 'Maths': 2, 'Pénébilite': 1}
partition = Partition()
partition.ajouter_groupe(Groupe(5))
partition.ajouter_groupe(Groupe(5))
partition.ajouter_groupe(Groupe(5))
partition.ajouter_groupe(Groupe(5))
# Appel de l'algorithme avec 3 groupes et des contraintes par genre 
partition = algo(
    eleves,
    partition
)

# Afficher la répartition finale des groupes
afficher_partition(partition)
