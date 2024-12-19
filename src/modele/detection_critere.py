from modele.criteres.booleen import Booleen
from modele.criteres.categorique import Categorique
from modele.criteres.numerique import Numerique

def detecter_type_critere(nom, valeurs):
    # Vérifier si toutes les valeurs sont des booléens (0 ou 1)
    if set(valeurs.dropna().unique()) <= {0, 1}:
        return Booleen(nom, 1, False)
    
    # Vérifier si chaque valeur a exactement 1 caractère
    if valeurs.dropna().apply(lambda x: isinstance(x, int) or (isinstance(x, str) and len(x) == 1)).all():
        return Numerique(nom,1, False)
    
    # Vérifier si les valeurs contiennent au moins 2 caractères
    if valeurs.dropna().apply(lambda x: len(str(x)) >= 2).all():
        return Categorique(nom, 1, False)
    
    raise ValueError(f"Impossible de déterminer le type pour le critère {nom}")