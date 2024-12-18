from modele.eleve import Eleve
from modele.critere import Critere
from modele.criteres.categorique import Categorique
from modele.criteres.booleen import Booleen
from modele.criteres.numerique import Numerique

def test1():
    critere1 = Numerique("Anglais",10)
    critere2 = Numerique("Francais",5)
    critere3 = Numerique("Math",3)
    [critere1.ajouter_valeur(i) for i in range(11)]
    [critere2.ajouter_valeur(i) for i in range(11)]
    [critere3.ajouter_valeur(i) for i in range(11)]
    eleves = generer_eleves([critere1,critere2,critere3], 100)
    print(eleves)
    pass
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
    for _ in range(nb):
        prenom = f"Prenom{random.randint(1, 1000)}"
        nom = f"Nom{random.randint(1, 1000)}"
        num_etudiant = random.randint(10000, 99999)
        genre = random.choice(['M', 'F'])
        eleve = Eleve(prenom, nom, num_etudiant, genre)
        for critere in criteres:
            minimum = min(critere.get_transpo().values())
            maximum = max(critere.get_transpo().values())
            eleve.ajouter_critere(critere, random.randint(minimum, maximum))
        eleves.append(eleve)
    return eleves
test1()