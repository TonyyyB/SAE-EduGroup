import tkinter as tk
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criteres = controller.criteres
        self.eleves = controller.eleves

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
        self.text_fields = {}  # Pour gérer les champs de texte

        for critere in self.criteres:
            # Créer un champ de texte pour chaque critère
            text_field = ctk.CTkEntry(self, width=50)  # Tu peux ajuster la largeur selon tes besoins
            text_field.insert(0, "1")
            text_field.place(relx=posx_menu -0.02, rely=posy_menu, anchor='center')
            
            # Ajouter un label à côté du champ de texte pour identifier le critère
            self.create_label(critere, posx_menu + 0.06, posy_menu, critere, font=PETITE_POLICE)
            
            # Stocker chaque champ de texte dans un dictionnaire pour référence ultérieure
            self.text_fields[critere] = text_field
            
            # Augmenter la position verticale pour le champ suivant
            posy_menu += 0.03

        # Bouton de génération avec font
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes)
        bouton_generer.place(relx=0.5, rely=0.9, anchor='center')

    def generer_groupes(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Affiche les niveaux sélectionnés pour chaque critère.
        """
        for critere, option_menu in self.option_menus.items():
            selection = option_menu.get()
            print(f"{critere}: {selection}")
        
        # Ajoutez ici le code pour générer les groupes ou effectuer une autre action