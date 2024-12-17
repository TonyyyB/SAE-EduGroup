from eleve import Eleve
from groupe import Groupe
from partition import Partition
from critere import Critere
from criteres.booleen import Booleen
from criteres.categorique import Categorique
from criteres.numerique import Numerique
import math

def algo(eleves:list|set[Eleve], partition:Partition):
    elevesAPlacer:set[Groupe] = set(eleves)
    groupes = partition.get_groupes()
    # Initialisation 
    for eleve in eleves:
        maxi = -math.inf
        gmax = None
        for groupe in groupes:
            if not groupe.respecter_contraintes(eleve) or not groupe.place_dispo(): continue
            score = groupe.simule_ajout(eleve)
            if score > maxi:
                maxi = score
                gmax = groupe
        if gmax is not None:
            gmax.ajouter_eleve(eleve)
            elevesAPlacer.remove(eleve)
    while len(elevesAPlacer) > 0:
        eleve = elevesAPlacer.pop()
        maxi = -math.inf
        gmax = None
        for groupe in groupes:
            if not groupe.place_dispo(): continue
            score = groupe.simule_ajout(eleve)
            if score > maxi:
                maxi = score
                gmax = groupe
        gmax.ajouter_eleve(eleve)
    # Boucle principale
    combinaisons:set[tuple[Groupe,Groupe]] = set()
    for groupe1 in groupes:
        for groupe2 in groupes:
            if groupe1 == groupe2: continue
            if (groupe2, groupe1) not in combinaisons:
                combinaisons.add((groupe1, groupe2))
                
    lastScore = partition.calcul_score()
    newScore = partition.calcul_score() + 1
    i = 0
    while(i < 100):
        lastScore = newScore
        for g1, g2 in combinaisons:
            groupeScoreInf = g1 if g1.calcul_score() < g2.calcul_score() else g2
            groupeScoreSup = g2 if groupeScoreInf == g1 else g1
            maxiEvolInf = 0
            evolMax = None
            for e1, e2 in zip(g1.get_eleves(), g2.get_eleves()):
                scoreGroupeInf, scoreGroupeSup = groupeScoreInf.simule_transf(groupeScoreSup, e1, e2)
                if scoreGroupeInf > groupeScoreInf.calcul_score():
                    if scoreGroupeInf > maxiEvolInf:
                        maxiEvolInf = scoreGroupeInf
                        evolMax = (e1, e2)
            if evolMax is not None:
                groupeScoreInf.transferer(groupeScoreSup, evolMax[0], evolMax[1])
        newScore = partition.calcul_score()
        i += 1
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

def afficher_partition(partition:Partition):
    """Affiche la répartition des élèves dans chaque groupe."""
    for i, groupe in enumerate(partition.groupes):
        print(f"Groupe {i+1} (Taille: {len(groupe.eleves)} / {groupe.taille}) Score: {groupe.calcul_score()}:")
        #for eleve in groupe.get_eleves():
        #    print(f"  - {eleve}")
        print()
def generer_eleves(criteres: list[Critere], nb: int) -> list[Eleve]:
    """Genere nb élèves aléatoirement

    Args:
        criteres (list[Critere]): liste des criteres
        nb (int): nombre d'élèves à génerer

    Returns:
        list[Eleve]: liste d'élèves
    """
    import random
    eleves = []
    for i in range(nb):
        prenom = f"Prenom{random.randint(1, 1000)}"
        nom = f"Nom{random.randint(1, 1000)}"
        num_etudiant = i
        genre = random.choice(['M', 'F'])
        eleve = Eleve(prenom, nom, num_etudiant, genre)
        for critere in criteres:
            minimum = min(critere.get_transpo().values())
            maximum = max(critere.get_transpo().values())
            eleve.ajouter_critere(critere, random.randint(minimum, maximum))
        eleves.append(eleve)
    return eleves
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
[x.ajouter_valeur(1) for x in [critereFrancais,critereMath,criterePenibilite]]
[x.ajouter_valeur(6) for x in [critereFrancais,critereMath,criterePenibilite]]
# Créer la liste des objets `Eleve`
eleves = []
#for data in donnees_eleves:
#    num_etudiant, nom, prenom, genre, francais, maths, penebilite = data
#    eleve = Eleve(prenom, nom, num_etudiant, genre)
#    eleve.ajouter_critere(critereFrancais, francais)
#    eleve.ajouter_critere(critereMath, maths)
#    penebilite_score = {"A": 1, "B": 2, "C": 3}.get(penebilite, 0)
#    eleve.ajouter_critere(criterePenibilite, penebilite_score)
#    eleves.append(eleve)

eleves.extend(generer_eleves([critereFrancais, critereMath, criterePenibilite],500))

# Coefficients de pondération pour chaque matière
partition = Partition()
g1 = Groupe(125)
g1.ajouter_contrainte(critereFrancais, {1, 3})

g2 = Groupe(125)
g2.ajouter_contrainte(critereFrancais, {2, 4})

g3 = Groupe(125)
g3.ajouter_contrainte(critereFrancais, {3, 5})

g4 = Groupe(125)
g4.ajouter_contrainte(critereFrancais, {4, 6})

partition.ajouter_groupe(g1)
partition.ajouter_groupe(g2)
partition.ajouter_groupe(g3)
partition.ajouter_groupe(g4)

# Appel de l'algorithme avec 3 groupes et des contraintes par genre 
partition = algo(
    eleves,
    partition
)

# Afficher la répartition finale des groupes
afficher_partition(partition)
