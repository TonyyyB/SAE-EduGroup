from eleve import Eleve
from groupe import Groupe
from partition import Partition
from critere import Critere
from criteres.booleen import Booleen
from criteres.categorique import Categorique
from criteres.numerique import Numerique
import math
import time
import random

def algo(eleves:list|set[Eleve], partition:Partition):
    elevesAPlacer:set[Groupe] = set(eleves)
    groupes = partition.get_groupes()
    # Initialisation
    for eleve in eleves:
        maxi = -math.inf
        gmax = None
        for groupe in groupes:
            if not groupe.respecter_contraintes(eleve) or not groupe.place_dispo(): continue
            score = partition.simule_ajout(groupe, eleve)
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
            score = partition.simule_ajout(groupe,eleve)
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
    newScore = lastScore + 1
    timeLastScoreNotGreater = 0
    while(timeLastScoreNotGreater < 3):
        lastScore = newScore
        for g1, g2 in combinaisons:
            newScore = partition.calcul_score()
            maxiEvol = 0
            evolMax = None
            for e1, e2 in zip(g1.get_eleves(), g2.get_eleves()):
                if not g1.respecter_contraintes(e2) or not g2.respecter_contraintes(e1): continue
                score = partition.simule_transf(g1, g2, e1, e2)
                if score > maxiEvol:
                    maxiEvol = score
                    evolMax = (g1, g2, e1, e2)
            if evolMax is not None:
                evolMax[0].transferer(evolMax[1], evolMax[2], evolMax[3])
        newScore = partition.calcul_score()
        if newScore > lastScore:
            #timeLastScoreNotGreater = 0
            pass
        else:
            timeLastScoreNotGreater += 1
    return partition

def afficher_partition(partition:Partition):
    """Affiche la répartition des élèves dans chaque groupe."""
    for i, groupe in enumerate(partition.groupes):
        print(f"Groupe {i+1} (Taille: {len(groupe.get_eleves())} / {groupe.taille}) Score: {groupe.calcul_score()}:")
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
    eleves = []
    for i in range(nb):
        prenom = f"Prenom{random.randint(1, 1000)}"
        nom = f"Nom{random.randint(1, 1000)}"
        num_etudiant = i
        genre = random.choice(["M", "F"])
        eleve = Eleve(prenom, nom, num_etudiant, genre)
        for critere in criteres:
            minimum = min(critere.get_transpo().values())
            maximum = max(critere.get_transpo().values())
            eleve.ajouter_critere(critere, random.randint(minimum, maximum))
        eleves.append(eleve)
    return eleves
critereFrancais = Numerique("Français",10, True)
critereMath = Numerique("Maths",5, True)
criterePenibilite = Numerique("Pénibilité", 3, True)
[x.ajouter_valeur(1) for x in [critereFrancais,critereMath,criterePenibilite]]
[x.ajouter_valeur(6) for x in [critereFrancais,critereMath,criterePenibilite]]

eleves = generer_eleves([critereFrancais, critereMath, criterePenibilite],200)

# Coefficients de pondération pour chaque matière
partition = Partition()
g1 = Groupe(50)
g1.ajouter_contrainte(critereFrancais, {1, 3})

g2 = Groupe(50)
g2.ajouter_contrainte(critereFrancais, {2, 4})

g3 = Groupe(50)
g3.ajouter_contrainte(critereFrancais, {3, 5})

g4 = Groupe(50)
g4.ajouter_contrainte(critereFrancais, {4, 6})

partition.ajouter_groupe(g1)
partition.ajouter_groupe(g2)
partition.ajouter_groupe(g3)
partition.ajouter_groupe(g4)
start = time.time()
# Appel de l'algorithme avec 3 groupes et des contraintes par genre
partition = algo(
    eleves,
    partition
)
stop = time.time()
# Afficher la répartition finale des groupes
afficher_partition(partition)
print(stop-start)
