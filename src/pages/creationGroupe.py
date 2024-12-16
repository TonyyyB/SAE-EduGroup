import tkinter as tk
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table

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
        self.setup_ui()  # Mettre à jour l'interface après le chargement des données

    def setup_ui(self):
        # Titre principal
        self.create_label("instruction_text", 0.5, 0.1, "Création du groupe", font=GRANDE_POLICE)

        # Tableau avec scrollbar (garder votre configuration de scrollbar)
        table = Table(parent=self, controller=self, eleves=self.eleves, criteres=self.criteres)
        table.place(relx=0.3, rely=0.5, anchor='center', relwidth=0.5, relheight=0.7)

        # Titre pour les groupes
        self.create_label("titre_groupe", 0.67, 0.23, "Affichage des groupes", font=MOYENNE_POLICE)

        # Affichage des groupes avec checkbox
        groupes = ["groupe1", "groupe2", "groupe3"]
        posx = 0.64
        posy = 0.27
        for groupe in groupes:
            checkbox = ctk.CTkCheckBox(master=self, text=groupe)
            checkbox.place(relx=posx, rely=posy, anchor='center')
            posy += 0.03  # Espacement entre les checkbox

        # Titre pour la priorité des critères
        self.create_label("ordre_prio", 0.89, 0.23, "Priorité des critères", font=MOYENNE_POLICE)

        # Champs de texte pour la priorité des critères
        posx_menu = 0.86
        posy_menu = 0.27

        for critere in self.criteres:
            # Créer un champ de texte pour chaque critère
            text_field = ctk.CTkEntry(self, width=50)  # Ajustez la largeur si nécessaire
            text_field.insert(0, "1")  # Valeur par défaut
            text_field.place(relx=posx_menu - 0.02, rely=posy_menu, anchor='center')

            # Ajouter un label pour identifier le critère
            self.create_label(critere, posx_menu + 0.06, posy_menu, critere, font=PETITE_POLICE)

            # Stocker chaque champ de texte dans un dictionnaire
            self.text_fields[critere] = text_field

            # Espacement entre les champs
            posy_menu += 0.03

        # Bouton de génération
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes)
        bouton_generer.place(relx=0.5, rely=0.9, anchor='center')

    def generer_groupes(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Affiche les niveaux sélectionnés pour chaque critère.
        """
        for critere, text_field in self.text_fields.items():
            priority = text_field.get()  # Récupère la valeur du champ
            print(f"{critere}: {priority}")
        
        # Ajoutez ici le code pour générer les groupes ou effectuer une autre action