import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
from pages.accueil import PageAccueil
from pages.page import Page
import pandas as pd
from Eleve import Eleve
from pages.creationGroupe import CreationGroupe

class App(TkinterDnD.Tk):  # Changement ici pour utiliser TkinterDnD.Tk
    def __init__(self, *args, **kwargs):
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
        for F in (PageAccueil,Page,CreationGroupe):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(PageAccueil)
    
    def show_frame(self, cont, eleves=None, criteres=None):
        # Montrer la page demandée
        frame = self.frames[cont]
        if eleves is not None and criteres is not None:
            frame.set_data(eleves, criteres)  # Si des données sont transmises, les passer à la page
        frame.tkraise()

# Initialiser et exécuter l'application
app = App()
app.mainloop()