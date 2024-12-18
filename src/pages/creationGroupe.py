import tkinter as tk
from Eleve import Eleve
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table
from pages.accueil import PageAccueil
from PIL import Image, ImageTk

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.eleves = []
        self.criteres = []
        self.text_fields = {}  # Pour gérer les champs de texte

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

    def clear_ui(self):
        """
        Méthode pour nettoyer l'interface en supprimant les éléments existants (labels, champs de texte, etc.).
        """
        for label in self.labels.values():
            label.destroy()  # Détruit les widgets existants
        self.labels.clear()  # Vide le dictionnaire des labels

        # Nettoyer les champs de texte
        for critere, text_field in self.text_fields.items():
            text_field.destroy()
        self.text_fields.clear()

        # Supprimer les anciens tableaux (groupes)
        for table in self.tables:
            table.destroy()  # Détruire chaque objet Table existant
        self.tables.clear()  # Réinitialiser la liste des tables

        # Supprimer le label des élèves restants s'il existe
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
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes)
        bouton_generer.place(relx=0.5, rely=0.9, anchor='center')

        # Bouton de retour
        bouton_exporter = ctk.CTkButton(self, text="Exporter les paramètres", font=GRANDE_POLICE, command=self.retour_page_accueil)
        bouton_exporter.place(relx=0.85, rely=0.10, anchor='center')

        # Bouton de retour
        bouton_resultats = ctk.CTkButton(self, text="Exporter les résultats", font=GRANDE_POLICE, command=self.retour_page_accueil)
        bouton_resultats.place(relx=0.85, rely=0.15, anchor='center')

        # Bouton de retour
        bouton_retour = ctk.CTkButton(self, text="Changer de fichier", font=GRANDE_POLICE, command=self.retour_page_accueil)
        bouton_retour.place(relx=0.85, rely=0.05, anchor='center')

    def decrease_group_count(self):
        """Réduit le nombre de groupes"""
        if self.nb_groupes > 1:  # Limite à 1 groupe minimum
            self.nb_groupes -= 1
            self.group_count_label.config(text=str(self.nb_groupes))
            self.generer_groupes_vides()  # Regénérer les groupes avec le nouveau nombre

    def increase_group_count(self):
        """Augmente le nombre de groupes"""
        self.nb_groupes += 1
        self.group_count_label.config(text=str(self.nb_groupes))
        self.generer_groupes_vides()  # Regénérer les groupes avec le nouveau nombre

    def generer_groupes_vides(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Affiche les niveaux sélectionnés pour chaque critère.
        """
        for critere, text_field in self.text_fields.items():
            priority = text_field.get()  # Récupère la valeur du champ
            print(f"{critere}: {priority}")
        
        # Ajoutez ici le code pour générer les groupes ou effectuer une autre action