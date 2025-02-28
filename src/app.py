import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
from pages.accueil import PageAccueil
from pages.page import Page
import pandas as pd
from modele.eleve import Eleve
from pages.creationGroupe import CreationGroupe

class App(TkinterDnD.Tk):  # Changement ici pour utiliser TkinterDnD.Tk
    def __init__(self, *args, **kwargs):
        # Initialiser TkinterDnD.Tk plutôt que tk.Tk
        TkinterDnD.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.Exit)
        
        self.title("EduGroup")
        
        # Définir la taille initiale de la fenêtre à 1280x1080
        self.geometry("1280x1080")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Ajouter les différentes pages ici
        for F in (PageAccueil, Page, CreationGroupe):
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

    def create_popup_window(self, title="Nouvelle fenêtre", size="400x300"):
        # Créer une nouvelle fenêtre pop-up
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry(size)
        
        # Exemple de contenu dans la fenêtre pop-up
        label = tk.Label(popup, text="Ceci est une fenêtre pop-up !")
        label.pack(pady=10)
        
        close_button = tk.Button(popup, text="Fermer", command=popup.destroy)
        close_button.pack(pady=10)
        
    def Exit(self):
        self.quit()

# Initialiser et exécuter l'application
app = App()
app.mainloop()