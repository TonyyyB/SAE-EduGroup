from modele.critere import Critere
from modele.eleve import Eleve
from modele.groupe import Groupe
from modele.partition import Partition

def algo(eleves,nb_groupes,tailles,contraintes):
    i = 0
    j = 0
    # A revoir
    for g in nb_groupes:
        groupe = Groupe(tailles[g])
    while i < len(eleves):
        while j < nb_groupes:
            #formule
            j += 1
        groupe.ajouterEleve(eleves[i])
    
    pass