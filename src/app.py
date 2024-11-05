import tkinter as tk
from tkinterdnd2 import TkinterDnD
from pages.accueil import PageAccueil
from pages.page import Page
from pages.creationGroupe import CreationGroupe  # Assurez-vous que l'import est correct

class App(TkinterDnD.Tk):  # Utilisation de TkinterDnD.Tk
    def __init__(self, *args, **kwargs):
        TkinterDnD.Tk.__init__(self, *args, **kwargs)
        
        self.title("EduGroup")
        
        # Définir la taille initiale de la fenêtre à 1400x1000
        self.geometry("1400x1000")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Ajouter les différentes pages ici
        for F in (PageAccueil, Page, CreationGroupe):  # Ajoutez CreationGroupe ici
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(PageAccueil)  # Démarrer avec la page d'accueil
    
    def show_frame(self, cont):
        # Montrer la page demandée
        frame = self.frames[cont]
        frame.tkraise()

# Initialiser et exécuter l'application
app = App()
app.mainloop()
