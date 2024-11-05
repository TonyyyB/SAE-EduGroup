import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from constantes import *
from pages.page import Page
from pages.creationGroupe import CreationGroupe

class PageAccueil(Page):
    def __init__(self, parent, controller):
        super().__init__(parent,controller)
        # Zone de dépôt de fichier centrée avec tkinterdnd2 + fonctionnalité de bouton
        self.frame = tk.Frame(self, bg='white', padx=10, pady=12, relief=tk.RIDGE, bd=5)
        self.frame.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.6, relheight=0.2)

        # Instruction centrée
        self.create_label("instruction_text", 0.5, 0.2, "Choisir le chemin du fichier :", font=GRANDE_POLICE)

        # Initialiser la fonctionnalité DnD pour la fenêtre Tkinter
        self.dnd_frame = self.frame
        self.dnd_frame.drop_target_register(DND_FILES)
        self.dnd_frame.dnd_bind('<<Drop>>', self.on_file_drop)

        # Lier la zone de dépôt à un clic pour ouvrir l'explorateur de fichiers
        self.frame.bind("<Button-1>", self.open_file_explorer)

        # Label dans la zone de dépôt/bouton
        self.drop_label = tk.Label(self.frame, text="Déposer le fichier ici ou cliquez pour choisir", bg='white', font=PETITE_POLICE)
        self.drop_label.pack(expand=True)

        # Bouton pour supprimer le fichier sélectionné
        self.clear_button = tk.Button(self.frame, text="❌", command=self.clear_file, bg='red', fg='white', font=PETITE_POLICE, width=2)
        self.clear_button.pack(side='right')

        # Boutons en bas de la fenêtre
        self.import_button = tk.Button(self, text="Importer des paramètres", command=self.import_params, bg='#3498DB', fg='white', font=MOYENNE_POLICE)
        self.import_button.place(relx=0.25, rely=0.8, anchor='center', relwidth=0.25, relheight=0.08)

        # Boutons pour créer les groupes
        self.create_button = tk.Button(self, text="Créer les groupes", command=self.go_to_next_page, bg='#3498DB', fg='white', font=MOYENNE_POLICE)
        self.create_button.place(relx=0.75, rely=0.8, anchor='center', relwidth=0.25, relheight=0.08)

    def create_gradient(self):
        super().create_gradient()

    def on_resize(self, event):
        self.create_gradient()

    def on_file_drop(self, event):
        # Nettoyer le chemin du fichier
        self.file_path = event.data.strip('{}')

        # Vérifier si le fichier est un CSV
        if self.file_path.endswith(".csv"):
            self.drop_label.config(text=f"Fichier ajouté : {self.file_path.split('/')[-1]}")
        else:
            # Alerte si ce n'est pas un fichier CSV
            self.file_path = None
            messagebox.showerror("Erreur", "Veuillez déposer uniquement des fichiers CSV.")
            self.drop_label.config(text="Déposer le fichier ici ou cliquez pour choisir")

    def open_file_explorer(self, event=None):
        # Ouvre l'explorateur de fichiers pour sélectionner un fichier CSV
        self.file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if self.file_path:
            if self.file_path.endswith(".csv"):
                self.drop_label.config(text=f"Fichier ajouté : {self.file_path.split('/')[-1]}")
            else:
                # Alerte si ce n'est pas un fichier CSV
                self.file_path = None
                messagebox.showerror("Erreur", "Veuillez sélectionner uniquement des fichiers CSV.")
                self.drop_label.config(text="Déposer le fichier ici ou cliquez pour choisir")

    def clear_file(self):
        self.file_path = None
        self.drop_label.config(text="Déposer le fichier ici ou cliquez pour choisir")

    def import_params(self):
        pass

    def go_to_next_page(self):
        if not self.file_path:
            messagebox.showwarning("Avertissement", "Veuillez ajouter un fichier avant de continuer.")
            return
        # Appel de la classe directement après avoir corrigé l'import
        self.controller.show_frame(CreationGroupe)
