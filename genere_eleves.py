import csv
import random

def generer_csv(n):
    headers = ["numEtudiant", "nom", "prenom", "genre", "niveauFrancais", "niveauMath", "penibilite", "handicape"]
    noms = ["Martin", "Bernard", "Deneau", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent"]
    prenoms = ["Jean", "Pierre", "Claire", "Andre", "Philippe", "Alain", "Louis", "Marc", "Paul", "Daniel"]
    genres = ["M", "F"]
    penibilites = ["A", "B", "C"]
    handicapes = ["OUI", "NON"]

    with open('eleves.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for i in range(1, n + 1):
            numEtudiant = i
            nom = random.choice(noms)
            prenom = random.choice(prenoms)
            genre = random.choice(genres)
            niveauFrancais = random.randint(1, 6)
            niveauMath = random.randint(1, 6)
            penibilite = random.choice(penibilites)
            handicape = random.choice(handicapes)
            
            writer.writerow([numEtudiant, nom, prenom, genre, niveauFrancais, niveauMath, penibilite, handicape])

generer_csv(200)