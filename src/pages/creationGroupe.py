import tkinter as tk
from modele.eleve import Eleve
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table
from pages.accueil import PageAccueil
from pages.parametreGroupe import ParametreGroupe
from PIL import Image, ImageTk

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.eleves = []
        self.criteres = []
        self.text_fields = {}
        self.labels = {}  # Pour stocker les labels créés sous forme de dictionnaire
        self.group_titles = []  # Liste pour garder une référence des labels de titres des groupes
        self.nb_groupes = 5
        self.tables = []  # Liste pour garder une référence des tables des groupes
        self.eleves_restants_label = None
        self.boutons_param = []  # Initialiser la liste pour les boutons de paramètres
        
        # Redimensionner l'image à la taille désirée
        self.img_param = Image.open("img/param.png")
        self.img_resized = self.img_param.resize((30, 30))  # Ajustez les dimensions selon vos besoins
        self.img_param_tk = ImageTk.PhotoImage(self.img_resized)

        # Ajouter un canvas pour le contenu
        self.canvas_frame = tk.Canvas(self.canvas)
        self.canvas_frame.place(relx=0.11, rely=0.22, relwidth=0.78, relheight=0.6)

        # Créer l'étiquette des élèves restants
        self.eleves_restants_label = tk.Label(self, text="Élèves restants: 0", font=("Arial", 16))
        self.eleves_restants_label.place(relx=0.15, rely=0.02, anchor='center')

        # Ajouter une scrollbar verticale pour le Canvas
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_y.set)

        # Créer un frame à l'intérieur du canvas
        self.inner_frame = tk.Frame(self.canvas_frame)
        self.canvas_frame.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Dessiner le fond dégradé sur la page (pas sur le canvas)
        self.create_gradient()
        self.generer_groupes_vides()

    def set_data(self, eleves, criteres):
        """
        Méthode pour définir les élèves et les critères depuis la page précédente.
        """
        self.eleves = eleves
        self.criteres = criteres
        self.clear_ui()  # Effacer l'interface existante avant de la recréer
        self.setup_ui()  # Mettre à jour l'interface après le chargement des données
        self.generer_groupes_vides()

    def clear_ui(self):
        """
        Méthode pour nettoyer l'interface en supprimant les éléments existants (labels, champs de texte, etc.).
        """
        # Supprimer les labels des titres des groupes
        for title_label in self.group_titles:
            title_label.destroy()  # Détruire les labels de titres des groupes
        self.group_titles.clear()  # Réinitialiser la liste des titres

        # Supprimer les autres éléments comme les champs de texte et les tableaux
        for label in self.labels.values():
            label.destroy()
        self.labels.clear()

        for critere, text_field in self.text_fields.items():
            text_field.destroy()
        self.text_fields.clear()

        for table in self.tables:
            table.destroy()
        self.tables.clear()

        # Supprimer les boutons de paramètres
        for bouton in self.boutons_param:
            bouton.destroy()
        self.boutons_param.clear()

        if self.eleves_restants_label:
            self.eleves_restants_label.destroy()

    def setup_ui(self):
        # Fixer la taille minimale de la fenêtre
        self.controller.geometry("1600x1000")
        self.controller.minsize(1600, 1000)

        # Titre principal
        label = self.create_label("instruction_text", 0.5, 0.05, "Création du groupe", font=GRANDE_POLICE)
        self.labels["instruction_text"] = label  # Ajoute le label avec une clé unique

        # Contrôle du nombre de groupes
        label_nb_groupes = self.create_label("label_nb_groupes", 0.15, 0.05, "Nombre de groupes", font=MOYENNE_POLICE)
        self.labels["label_nb_groupes"] = label_nb_groupes

        # Affichage du nombre de groupes avec boutons +
        group_control_frame = tk.Frame(self)
        group_control_frame.place(relx=0.15, rely=0.1, anchor='center')

        decrease_button = ctk.CTkButton(group_control_frame, text="-", font=("Arial", 16), command=self.decrease_group_count)
        decrease_button.grid(row=0, column=0)

        self.group_count_label = tk.Label(group_control_frame, text=str(self.nb_groupes), font=("Arial", 16), width=5, height=2, relief="solid")
        self.group_count_label.grid(row=0, column=1)

        increase_button = ctk.CTkButton(group_control_frame, text="+", font=("Arial", 16), command=self.increase_group_count)
        increase_button.grid(row=0, column=2)

        # Ajouter le compteur d'élèves restants
        self.eleves_restants_label = tk.Label(self, text=f"Élèves restants: {len(self.eleves)}", font=("Arial", 16))
        self.eleves_restants_label.place(relx=0.15, rely=0.02, anchor='center')

        # Bouton de génération
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes_vides)
        bouton_generer.place(relx=0.5, rely=0.12, anchor='center')

    def generer_groupes(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Affiche les niveaux sélectionnés pour chaque critère.
        """
        for critere, text_field in self.text_fields.items():
            priority = text_field.get()  # Récupère la valeur du champ
            print(f"{critere}: {priority}")
        
        # Ajoutez ici le code pour générer les groupes ou effectuer une autre action