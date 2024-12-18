import tkinter as tk
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table
from pages.creationGroupe import CreationGroupe

class ParametreGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.eleves = []
        self.criteres = []
        self.text_fields = {}  # Pour gérer les champs de texte
        self.labels = {}  # Pour stocker les labels créés sous forme de dictionnaire
        self.nb_groupes = 5  # Initialisation du nombre de groupes à 5
        self.tables = []  # Liste pour garder une référence des tables des groupes
        self.eleves_restants_label = None  # Label pour afficher le nombre d'élèves restants

        # Ajouter un canvas pour le contenu
        self.canvas_frame = tk.Canvas(self.canvas)
        self.canvas_frame.place(relx=0.11, rely=0.22, relwidth=0.78, relheight=0.6)

        # Ajouter une scrollbar verticale pour le Canvas
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_y.set)

        # Créer un frame à l'intérieur du canvas
        self.inner_frame = tk.Frame(self.canvas_frame)
        self.canvas_frame.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Dessiner le fond dégradé sur la page (pas sur le canvas)
        self.create_gradient()

    def set_data(self, eleves, criteres):
        """
        Méthode pour définir les élèves et les critères depuis la page précédente.
        """
        self.eleves = eleves
        self.criteres = criteres
        self.clear_ui()  # Effacer l'interface existante avant de la recréer
        self.setup_ui()  # Mettre à jour l'interface après le chargement des données

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
        bouton_generer.place(relx=0.5, rely=0.12, anchor='center')

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

    def increase_group_count(self):
        """Augmente le nombre de groupes"""
        self.nb_groupes += 1
        self.group_count_label.config(text=str(self.nb_groupes))

    def generer_groupes(self):
        """
        Action lors de l'appui sur le bouton "Générer les groupes".
        Répartit les élèves dans les groupes et les affiche dans un tableau.
        """
        self.scrollbar_y.destroy()
        for table in self.tables:
            table.destroy()  # Détruire chaque objet Table existant
        self.tables.clear()  # Réinitialiser la liste des tables

        total_eleves = len(self.eleves)
        groupes = {f'Groupe {i+1}': [] for i in range(self.nb_groupes)}

        for i, eleve in enumerate(self.eleves):
            groupe_num = i % self.nb_groupes
            groupes[f'Groupe {groupe_num + 1}'].append(eleve)

        eleves_restants = total_eleves % self.nb_groupes
        self.eleves_restants_label.config(text=f"Élèves restants: {eleves_restants}")

        self.inner_frame.update_idletasks()

        nb_colonnes = 3
        espacement = 10
        posx, posy = 0, 0

        for i, (groupe_name, eleves_in_groupe) in enumerate(groupes.items()):
            # Ajouter un titre avec fond bleu (3D83B1) et texte blanc
            title_label = tk.Label(self.inner_frame, text=groupe_name, font=("Arial", 12, "bold"), 
                                bg="#3D83B1", fg="white", width=15, height=2, anchor="center")
            title_label.grid(row=posy, column=posx, padx=espacement, pady=espacement)

            # Créer la table pour chaque groupe
            table = Table(parent=self.inner_frame, controller=self, eleves=eleves_in_groupe, criteres=self.criteres)
            table.grid(row=posy + 1, column=posx, padx=espacement, pady=espacement)

            # Personnalisation des cellules du tableau
            for widget in table.winfo_children():  # Parcourir tous les widgets enfants de la table
                if isinstance(widget, tk.Label):  # S'assurer qu'il s'agit d'un Label
                    widget.config(bg="white", fg="black", relief="solid", bd=1)  # Cellules blanches avec contour gris et texte noir

            self.tables.append(table)

            posx += 1
            if posx >= nb_colonnes:
                posx = 0
                posy += 2  # Décaler de 2 lignes pour séparer le titre du tableau

        self.inner_frame.update_idletasks()
        self.canvas_frame.config(scrollregion=self.canvas_frame.bbox("all"))

        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_y.set)


    def retour_page_accueil(self):
        """
        Retourne à la page d'accueil.
        """
        self.controller.show_frame(CreationGroupe)  # Retour à la page d'accueil