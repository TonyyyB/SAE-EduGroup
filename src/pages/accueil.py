import tkinter as tk
from tkinter import filedialog, messagebox
import unicodedata
from tkinterdnd2 import DND_FILES
import customtkinter as ctk
from constantes import *
from pages.page import Page
import pandas as pd
from modele.eleve import Eleve
from modele.critere import Critere

class PageAccueil(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Zone de dépôt de fichier centrée avec tkinterdnd2 + fonctionnalité de bouton
        self.frame = tk.Frame(self, bg='white', padx=10, pady=12, relief=tk.RIDGE, bd=5)
        self.frame.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.6, relheight=0.2)

        # Instruction centrée
        self.create_label("instruction_text", 0.5, 0.2, "Choisir le chemin du fichier :", font=GRANDE_POLICE, fill="white")

        # Initialiser la fonctionnalité DnD pour la fenêtre Tkinter
        self.dnd_frame = self.frame
        self.dnd_frame.drop_target_register(DND_FILES)
        self.dnd_frame.dnd_bind('<<Drop>>', self.on_file_drop)

        # Lier la zone de dépôt à un clic pour ouvrir l'explorateur de fichiers
        self.frame.bind("<Button-1>", self.open_file_explorer)

        # Bouton dans la zone de dépôt (il remplace le label)
        self.drop_button = ctk.CTkButton(self.frame, text="Déposer le fichier ici ou cliquez pour choisir", 
                                         font=PETITE_POLICE, fg_color='transparent', hover_color='#f0f0f0',
                                         text_color='black' ,command=self.open_file_explorer)
        self.drop_button.pack(expand=True)

        # Bouton pour supprimer le fichier sélectionné
        self.clear_button = tk.Button(self.frame, text="❌", command=self.clear_file, bg='red', fg='white', font=PETITE_POLICE, width=2)
        self.clear_button.pack(side='right')

        # Bouton pour créer les groupes
        self.create_button = tk.Button(self, text="Créer les groupes", command=self.go_to_next_page, bg='#3498DB', fg='white', font=MOYENNE_POLICE)
        self.create_button.place(relx=0.5, rely=0.8, anchor='center', relwidth=0.25, relheight=0.08)

    def on_file_drop(self, event):
        # Nettoyer le chemin du fichier
        self.file_path = event.data.strip('{}')

        # Vérifier si le fichier est un CSV
        if self.file_path.endswith(".csv"):
            self.drop_button.configure(text=f"Fichier ajouté : {self.file_path.split('/')[-1]}")
        else:
            # Alerte si ce n'est pas un fichier CSV
            self.file_path = None
            messagebox.showerror("Erreur", "Veuillez déposer uniquement des fichiers CSV.")
            self.drop_button.configure(text="Déposer le fichier ici ou cliquez pour choisir")

    def open_file_explorer(self, event=None):
        # Ouvre l'explorateur de fichiers pour sélectionner un fichier CSV
        self.file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if self.file_path:
            if self.file_path.endswith(".csv"):
                self.drop_button.configure(text=f"Fichier ajouté : {self.file_path.split('/')[-1]}")
            else:
                # Alerte si ce n'est pas un fichier CSV
                self.file_path = None
                messagebox.showerror("Erreur", "Veuillez sélectionner uniquement des fichiers CSV.")
                self.drop_button.configure(text="Déposer le fichier ici ou cliquez pour choisir")

    def clear_file(self):
        # Effacer le chemin du fichier
        self.file_path = None
        
        # Remettre le texte par défaut du bouton drop_button
        self.drop_button.configure(text="Déposer le fichier ici ou cliquez pour choisir")

    def import_params(self):
        pass

    def go_to_next_page(self):
        if not self.file_path:
            messagebox.showwarning("Avertissement", "Veuillez ajouter un fichier avant de continuer.")
            return
        
        # Charger les élèves et les critères à partir du CSV
        df = pd.read_csv(self.file_path)

        def normaliser_colonnes(colonnes):
            """
            Normalise les noms des colonnes pour qu'ils soient en minuscules,
            sans accents, ni caractères spéciaux, et remplace les espaces par des underscores.

            :param colonnes: Liste des noms de colonnes.
            :return: Liste des noms de colonnes normalisés.
            """
            return [
                ''.join(
                    c for c in unicodedata.normalize('NFD', col.lower())
                    if c.isalnum() or c == ' '
                ).replace(' ', '_')
                for col in colonnes
            ]
        df.columns = normaliser_colonnes(df.columns)
        self.criteres:list[Critere] = []
        for critere in df.columns[4:]:
            self.criteres.append(Critere(critere,5, set(df[critere])))

        # Créer la liste des élèves
        import random
        self.eleves = []
        for _, row in df.iterrows():
            eleve = Eleve(prenom=row['prenom'], nom=row['nom'], num_etudiant=row['numetudiant'], genre=row['genre'])
            for critere in self.criteres:
                eleve.ajouter_critere(critere, row[critere.get_nom()])
            self.eleves.append(eleve)
        
        # Charger dynamiquement la page CreationGroupe en passant les élèves et les critères
        from pages.creationGroupe import CreationGroupe  # Import dynamique
        self.controller.show_frame(CreationGroupe, self.eleves, self.criteres)
