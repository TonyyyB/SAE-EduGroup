import tkinter as tk
from modele.eleve import Eleve
from modele.partition import Partition
from modele.groupe import Groupe
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table
from pages.accueil import PageAccueil
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.eleves = []
        self.criteres = []
        self.text_fields = {}
        self.nb_groupes = 5
        self.tables = []  # Liste pour garder une référence des tables des groupes
        self.eleves_restants_label = None
        
        # Redimensionner l'image à la taille désirée
        self.img_param = Image.open("img/param.png")
        self.img_resized = self.img_param.resize((30, 30))  # Ajustez les dimensions selon vos besoins
        self.img_param_tk = ImageTk.PhotoImage(self.img_resized)

        # Ajouter un canvas pour le contenu
        self.canvas_frame = tk.Canvas(self.canvas)
        self.canvas_frame.place(relx=0.11, rely=0.22, relwidth=0.78, relheight=0.6)

        # Ajouter une scrollbar verticale pour le Canvas
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        # Créer un frame à l'intérieur du canvas
        self.inner_frame = tk.Frame(self.canvas_frame)
        self.canvas_frame.create_window((0, 0), window=self.inner_frame, anchor="nw")

    def set_data(self, eleves, criteres):
        """
        Méthode pour définir les élèves et les critères depuis la page précédente.
        """
        self.eleves = eleves
        self.criteres = criteres
        # Créer la partition
        self.partition = Partition(self.eleves)
        # Créer les groupes par défaut
        for i in range(self.nb_groupes):
            groupe = Groupe(20)
            self.partition.ajouter_groupe(groupe)
        self.partition.adapter_taille()
        self.clear_ui()  # Effacer l'interface existante avant de la recréer
        self.setup_ui()  # Mettre à jour l'interface après le chargement des données
        self.afficher_groupes()

    def clear_ui(self):
        """
        Méthode pour nettoyer l'interface en supprimant les éléments existants (dict_labels, champs de texte, etc.).
        """

        for critere, text_field in self.text_fields.items():
            text_field.destroy()
        self.text_fields.clear()

        for table in self.tables:
            table.destroy()
        self.tables.clear()

        self.clear_labels()

        if self.eleves_restants_label:
            self.eleves_restants_label.destroy()

    def setup_ui(self):
        # Fixer la taille minimale de la fenêtre
        self.controller.geometry("1600x1000")
        self.controller.minsize(1600, 1000)

        # Titre principal
        self.create_label("instruction_text", 0.5, 0.05, "Création du groupe", font=GRANDE_POLICE)

        # Contrôle du nombre de groupes
        self.create_label("label_nb_groupes", 0.15, 0.05, "Nombre de groupes", font=MOYENNE_POLICE)

        # Affichage du nombre de groupes avec boutons +
        group_control_frame = tk.Frame(self)
        group_control_frame.place(relx=0.15, rely=0.1, anchor='center')

        decrease_button = ctk.CTkButton(group_control_frame, text="-", font=("Arial", 16), command=self.decrease_group_count)
        decrease_button.grid(row=0, column=0)

        self.group_count_label = tk.Label(group_control_frame, text=str(self.nb_groupes), font=("Arial", 16), width=5, height=2, relief="solid")
        self.group_count_label.grid(row=0, column=1)

        increase_button = ctk.CTkButton(group_control_frame, text="+", font=("Arial", 16), command=self.increase_group_count)
        increase_button.grid(row=0, column=2)

        self.create_label("eleves_restants", 0.15, 0.02, text=f"Élèves restants: {len(self.eleves)}", font=MOYENNE_POLICE)

        # Bouton de génération
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes)
        bouton_generer.place(relx=0.5, rely=0.12, anchor='center')

        # Bouton de retour
        bouton_exporter = ctk.CTkButton(self, text="Exporter les paramètres", font=GRANDE_POLICE, command=self.retour_page_accueil)
        bouton_exporter.place(relx=0.85, rely=0.10, anchor='center')

        # Bouton de retour
        bouton_param = ctk.CTkButton(self, text="Paramètres des critères", font=GRANDE_POLICE, command=self.pop_up_criteres)
        bouton_param.place(relx=0.15, rely=0.17, anchor='center')

        # Bouton paramètres groupes
        self.bouton_parm_grp = None

        # Bouton de retour
        bouton_resultats = ctk.CTkButton(self, text="Exporter les résultats", font=GRANDE_POLICE, command=self.retour_page_accueil)
        bouton_resultats.place(relx=0.85, rely=0.15, anchor='center')

        # Bouton de retour
        bouton_retour = ctk.CTkButton(self, text="Changer de fichier", font=GRANDE_POLICE, command=self.retour_page_accueil)
        bouton_retour.place(relx=0.85, rely=0.05, anchor='center')
    
    def generer_groupes(self):
        self.partition.generer()
        self.afficher_groupes()

    def decrease_group_count(self):
        """Réduit le nombre de groupes"""
        if self.nb_groupes > 1:  # Limite à 1 groupe minimum
            self.nb_groupes -= 1
            self.partition.supprimer_groupe(self.partition.get_groupes()[-1])
            self.partition.adapter_taille()
            self.group_count_label.config(text=str(self.nb_groupes))
            self.afficher_groupes()  # Regénérer les groupes avec le nouveau nombre

    def increase_group_count(self):
        """Augmente le nombre de groupes"""
        self.nb_groupes += 1
        self.partition.ajouter_groupe(Groupe(20))
        self.partition.adapter_taille()
        self.group_count_label.config(text=str(self.nb_groupes))
        self.afficher_groupes()  # Regénérer les groupes avec le nouveau nombre

    def afficher_groupes(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Répartit les élèves dans les groupes et les affiche dans un tableau.
        """
        # Détruire les anciens groupes et labels
        self.scrollbar_y.destroy()
        for table in self.tables:
            table.destroy()  # Détruire chaque objet Table existant
        self.tables.clear()  # Réinitialiser la liste des tables


        self.change_text("eleves_restants", f"Élèves restants: {len(self.eleves)}")

        self.inner_frame.update_idletasks()

        nb_colonnes = 3
        posx, posy = 0, 0

        for i, groupe in enumerate(self.partition.get_groupes()):
            tg = TableauGroupe(self.inner_frame, self.partition, i, self.img_param_tk)
            tg.grid(row=posy, column=posx)

            self.tables.append(tg)

            posx += 1
            if posx >= nb_colonnes:
                posx = 0
                posy += 2  # Décaler de 2 lignes pour séparer le titre du tableau

        self.inner_frame.update_idletasks()
        self.canvas_frame.config(scrollregion=self.canvas_frame.bbox("all"))

        if self.scrollbar_y is not None:
            self.scrollbar_y.pack_forget()  # Désinstaller la scrollbar si elle est déjà présente
            self.scrollbar_y.destroy()
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_y.set)


    def retour_page_accueil(self):
        """
        Retourne à la page d'accueil.
        """
        self.controller.show_frame(PageAccueil)  # Retour à la page d'accueil

    def pop_up_criteres(self):
        """
        Méthode pour ouvrir un pop-up qui permet de paramétrer les critères.
        """
        from pages.parametresCriteres import ParametresCriteres
        popup = ParametresCriteres(self, self.criteres)  # Passage des critères à la classe ParametresCriteres
        popup.grab_set()  # Pour forcer le focus sur la fenêtre pop-up

    def pop_up_param_grp(self, groupe):
        from pages.parametresGroupe import ParametresGroupe
        popup = ParametresGroupe(self, self.partition, groupe)
        popup.grab_set()  # Pour forcer le focus sur la fenêtre pop-up

class TableauGroupe(tk.Frame):
    def __init__(self, parent, partition:Partition, index, img_param_tk):
        super().__init__(parent)
        self.groupe = partition.get_groupes()[index]
        self.partition = partition
        title_label = tk.Label(self, text=f"Groupe {index+1}", font=("Arial", 12, "bold"), 
                                    bg="#3D83B1", fg="white", width=15, height=2, anchor="center")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Créer le bouton avec l'image redimensionnée
        bouton_param_grp = tk.Button(self, image=img_param_tk, compound="right", anchor='e', command=lambda: self.pop_up_param_grp())
        bouton_param_grp.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        # Créer la table pour chaque groupe
        table = Table(parent=self, controller=self, eleves=self.groupe.get_eleves(), criteres=self.partition.get_criteres())
        table.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        # Personnalisation des cellules du tableau
        for widget in table.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="white", fg="black", relief="solid", bd=1)
    def pop_up_param_grp(self):
        from pages.parametresGroupe import ParametresGroupe
        popup = ParametresGroupe(self, self.partition, self.groupe)
        popup.grab_set()  # Pour forcer le focus sur la fenêtre pop-up