import tkinter as tk
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table


class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Titre principal
        self.create_label("instruction_text", 0.5, 0.1, "Création du groupe", font=GRANDE_POLICE)

        # Tableau avec scrollbar (garder votre configuration de scrollbar)
        tableau = Table(self, controller, 50, 4, ["Nom", "Type", "Minimal", "Maximal"])
        tableau.place(relx=0.3, rely=0.35, anchor='center', relwidth=0.5, relheight=0.3)

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

        # Menu déroulant pour la priorité des critères
        criteres = ['niveau français', 'niveau anglais', 'niveau chinois']
        posx_menu = 0.86
        posy_menu = 0.27
        options = [''] + [str(i+1) for i in range(len(criteres))]  # Conversion des options en chaînes de caractères
        self.option_menus = {}  # Pour gérer les menus déroulants
        for critere in criteres:
            option_menu = ctk.CTkOptionMenu(self, values=options, width=15)
            option_menu.place(relx=posx_menu, rely=posy_menu, anchor='center')
            self.create_label(critere, posx_menu + 0.06, posy_menu, critere, font=PETITE_POLICE)
            self.option_menus[critere] = option_menu
            posy_menu += 0.03

        # Bouton de génération avec font
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes)
        bouton_generer.place(relx=0.5, rely=0.6, anchor='center')

    def generer_groupes(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Affiche les niveaux sélectionnés pour chaque critère.
        """
        for critere, option_menu in self.option_menus.items():
            selection = option_menu.get()
            print(f"{critere}: {selection}")
        
        # Ajoutez ici le code pour générer les groupes ou effectuer une autre action