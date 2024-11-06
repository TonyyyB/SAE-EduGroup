import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
from pages.accueil import PageAccueil
from pages.page import Page
import pandas as pd
from Eleve import Eleve

class App(TkinterDnD.Tk):  # Changement ici pour utiliser TkinterDnD.Tk
    def __init__(self, *args, **kwargs):
        # Instancier les élèves
        df = pd.read_csv('doc.csv')
        self.criteres = df.columns.to_list()[5:]

        # Créer une liste d'élèves
        self.eleves = []

        # Parcourir chaque ligne du CSV et instancier un objet Eleve
        for _, row in df.iterrows():
            # Instancier un élève avec les informations de base
            eleve = Eleve(prenom=row['Prénom'], nom=row['Nom'], num_etudiant=row['NumÉtudiant'], genre=row['Genre'])
            
            # Ajouter les matières et les notes à l'élève, dynamiquement
            for critere in self.criteres:
                eleve.ajouter_critere(critere, row[critere])
            
            # Ajouter l'élève à la liste
            self.eleves.append(eleve)

        

        # Initialiser TkinterDnD.Tk plutôt que tk.Tk
        TkinterDnD.Tk.__init__(self, *args, **kwargs)
        
        self.title("EduGroup")
        
        # Définir la taille initiale de la fenêtre à 1280x1080
        self.geometry("1400x1000")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Ajouter les différentes pages ici
        for F in (PageAccueil,Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(PageAccueil)
    
    def show_frame(self, cont):
        # Montrer la page demandée
        frame = self.frames[cont]
        frame.tkraise()

# Initialiser et exécuter l'application
app = App()
app.mainloop()