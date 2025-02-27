import json
import tkinter as tk
import tkinter.font as tkf
import csv
from tkinter import filedialog
from modele.eleve import Eleve
from modele.partition import Partition
from modele.groupe import Groupe
import customtkinter as ctk
from constantes import *
from pages.page import Page
from pages.page import Table, EleveTable
from pages.accueil import PageAccueil
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk
import threading
from itertools import cycle

class CreationGroupe(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.groupes = []
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
        self.canvas_frame.place(relx=0.4, rely=0.25, relwidth=0.53, relheight=0.7)

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
        self.afficher_criteres()

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

        decrease_button = ctk.CTkButton(group_control_frame, text="-", font=("Arial", 16), command=self.decrease_group_count, corner_radius=0, width=90, height=40)
        decrease_button.grid(row=0, column=0)

        self.group_count_label = tk.Label(group_control_frame, text=str(self.nb_groupes), font=("Arial", 16), width=14, height=1)
        self.group_count_label.grid(row=0, column=1)

        increase_button = ctk.CTkButton(group_control_frame, text="+", font=("Arial", 16), command=self.increase_group_count, corner_radius=0,width=90, height=40)
        increase_button.grid(row=0, column=2)

        self.create_label("eleves_restants", 0.15, 0.02, text=f"Élèves restants: {len(self.eleves)}", font=MOYENNE_POLICE)

        # Bouton de génération
        bouton_generer = ctk.CTkButton(self, text="Générer les groupes", font=GRANDE_POLICE, command=self.generer_groupes, corner_radius=0,height=80, width=500)
        bouton_generer.place(relx=0.5, rely=0.12, anchor='center')


        # Bouton paramètres groupes
        self.bouton_parm_grp = None

        # Bouton de retour
        bouton_retour = ctk.CTkButton(self, text="Changer de fichier", font=GRANDE_POLICE, command=self.retour_page_accueil, corner_radius=0,width=350)
        bouton_retour.place(relx=0.15, rely=0.16, anchor='center')

        # Bouton de retour
        bouton_resultats = ctk.CTkButton(self, text="Exporter les résultats", font=GRANDE_POLICE, command=self.exporter_groupes, corner_radius=0,width=400)
        bouton_resultats.place(relx=0.7, rely=0.09, anchor='sw')

        # Bouton en bas pour importer les paramètres
        import_button = ctk.CTkButton(self, text="Importer des paramètres", font=GRANDE_POLICE, command=self.importer_criteres, corner_radius=0,width=400)
        import_button.place(relx=0.7, rely=0.15, anchor='sw')

        # Bouton exporter
        bouton_exporter = ctk.CTkButton(self, text="Exporter les paramètres", font=GRANDE_POLICE, command=self.exporter_criteres, corner_radius=0,width=400)
        bouton_exporter.place(relx=0.7, rely=0.21, anchor='sw')

    def generer_groupes(self):
        self.loading_popup = tk.Toplevel(self)
        self.loading_popup.title("Chargement...")
        self.loading_popup.geometry("250x120")
        self.loading_popup.transient(self)
        self.loading_popup.config(bg="white")


        self.loading_popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (250 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (120 // 2)
        self.loading_popup.geometry(f"+{x}+{y}")

        self.loading_label = tk.Label(self.loading_popup, text="Chargement", font=("Arial", 12), bg="white")
        self.loading_label.pack(pady=10)

        self.info_label = tk.Label(self.loading_popup, text="Veuillez patienter...", font=("Arial", 10), fg="gray", bg="white")
        self.info_label.pack()

        self.loading_states = cycle(["Chargement", "Chargement.", "Chargement..", "Chargement..."])

        self.animate_loading()

        self.loading_popup.grab_set()
        self.loading_popup.update()

        thread = threading.Thread(target=self.partition.generer)
        thread.start()

        self.check_task_completion(thread)

    def animate_loading(self):
        self.loading_label.config(text=next(self.loading_states))
        self.loading_label.update_idletasks()
        if hasattr(self, "loading_popup") and self.loading_popup.winfo_exists():
            self.loading_popup.after(300, self.animate_loading)

    def check_task_completion(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_task_completion(thread))
        else:
            self.loading_popup.grab_release()
            self.afficher_groupes()
            self.loading_popup.destroy()

    def exporter_groupes(self):
        """
        Exporte les groupes et leurs élèves dans un fichier CSV.
        """
        fichier = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not fichier:
            return
        
        data = []

        for i, groupe in enumerate(self.partition.get_groupes(), start=1):
            for eleve in groupe.get_eleves():
                data.append({
                    "Nom": eleve.nom,
                    "Prénom": eleve.prenom,
                    "Groupe": f"{i}"
                })

        df = pd.DataFrame(data)
        df.to_csv(fichier, index=False, encoding='utf-8')
        print(f"Exportation réussie : {fichier}")

    def decrease_group_count(self):
        """Réduit le nombre de groupes"""
        if self.nb_groupes > 2:  # Limite à 2 groupe minimum
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
    
    def exporter_criteres(self):
        """
        Exporte les critères, leurs valeurs et les contraintes des groupes sous forme de JSON.
        """
        fichier = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Exporter les critères"
        )

        if not fichier:
            return

        # Récupération des valeurs des sliders avec contraintes des groupes
        data = []
        for i, groupe in enumerate(self.partition.get_groupes(), start=1):
            groupe_data = {
                "groupe": i,
                "criteres": []
            }
            for critere in self.criteres:
                contrainte = groupe.get_contrainte(critere)
                contrainte_str = ", ".join(map(str, contrainte)) if contrainte else "N/A"
                groupe_data["criteres"].append({
                    "nom": critere.get_nom(),
                    "valeur": critere.get_poids(),
                    "contrainte": contrainte_str
                })
            data.append(groupe_data)

        try:
            with open(fichier, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            print(f"Exportation réussie : {fichier}")
            messagebox.showinfo("Exportation réussie", f"Les critères ont été exportés avec succès dans {fichier}.")

        except Exception as e:
            print(f"Erreur lors de l'exportation : {e}")
            messagebox.showerror("Erreur d'exportation", f"Une erreur est survenue : {e}")

        return data  # Retourne les données sous forme de JSON

    def importer_criteres(self):
        # Dictionnaire des critères existants
        criteres = {critere.get_nom(): critere for critere in self.criteres}
        
        # Ouvrir une boîte de dialogue pour sélectionner un fichier JSON
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")])
        if filepath:
            if not filepath.endswith(".json"):
                messagebox.showerror("Erreur", "Veuillez sélectionner un fichier JSON.")
                return
            
            try:
                # Lire le fichier JSON
                with open(filepath, mode='r', encoding='utf-8') as file:
                    data = json.load(file)
                print(f"Importation réussie : {filepath}")
            except Exception as e:
                print(f"Erreur lors de l'importation : {e}")
                return

            # Vérifier si le fichier contient des données
            if not data:
                return messagebox.showerror("Erreur", "Aucune donnée à importer.")

            # Déterminer le nombre de groupes dans le fichier JSON
            nombre_de_groupes = len(data)
            print(f"Nombre de groupes détectés : {nombre_de_groupes}")

            # Mettre à jour le nombre de groupes dans la Partition
            self.mettre_a_jour_nombre_de_groupes(nombre_de_groupes)

            # Traiter chaque groupe
            for i, groupe_data in enumerate(data):
                groupe = self.groupes[i]  # Récupérer le groupe correspondant
                for critere_data in groupe_data['criteres']:
                    nom_critere = critere_data['nom']
                    valeur = critere_data['valeur']
                    contrainte = critere_data['contrainte']

                    # Vérifier si le critère existe
                    if nom_critere not in criteres:
                        print(f"Critère non reconnu : {nom_critere}")
                        continue

                    # Appliquer la valeur du critère
                    critere = criteres[nom_critere]
                    critere.set_poids(valeur)

                    # Appliquer les contraintes
                    if contrainte != "N/A":
                        contrainte_valeurs = set(map(int, contrainte.split(", ")))
                        groupe.set_contrainte(critere, contrainte_valeurs)

            # Afficher les critères mis à jour
            self.afficher_criteres()

    def mettre_a_jour_nombre_de_groupes(self, nombre_de_groupes):
        """
        Met à jour le nombre de groupes dans la Partition.
        """
        # Supprimer les groupes existants si nécessaire
        self.partition.groupes.clear()

        # Ajouter de nouveaux groupes
        for _ in range(nombre_de_groupes):
            nouveau_groupe = Groupe(taille=0)  # Crée un groupe avec une taille par défaut
            self.groupes.append(nouveau_groupe)

        print(f"Nombre de groupes mis à jour : {nombre_de_groupes}")

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

        restant = len(self.partition.eleves)
        for groupe in self.partition.get_groupes():
            restant -= len(groupe.eleves)
            print(restant)
        
        self.change_text("eleves_restants", text=f"Élèves restants: {restant}")        

        self.inner_frame.update_idletasks()

        nb_colonnes = 2
        posx, posy = 0, 0

        for i, groupe in enumerate(self.partition.get_groupes()):
            tg = TableauGroupe(self.inner_frame, self, self.partition, i, self.img_param_tk)
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

    def afficher_criteres(self):
        table = TableauCriteres(self, self, self.criteres)
        table.place(relx=0.05, rely=0.3)

    def retour_page_accueil(self):
        """
        Retourne à la page d'accueil.
        """
        self.controller.show_frame(PageAccueil)  # Retour à la page d'accueil


    def pop_up_param_grp(self, groupe):
        from pages.parametresGroupe import ParametresGroupe
        popup = ParametresGroupe(self, self.partition, groupe)
        popup.grab_set()  # Pour forcer le focus sur la fenêtre pop-up


class TableauCriteres(tk.Frame):
    def __init__(self, parent, page, criteres):
        super().__init__(parent, background='')
        self.criteres = criteres
        self.page = page
        self.table = Table(parent=self, controller=self)
        self.table._create_table_headers(["Critère","", "Val"])
        self.table.grid(row=0, column=0, padx=10, pady=10)
        self.sliders = []
        self.sliders_vars = []

        for i, critere in enumerate(self.criteres):
            poids_var = tk.IntVar(value=critere.get_poids())
            poids_scale = tk.Scale(self.table.frame, variable=poids_var, from_=0, to=100, resolution=1, orient="horizontal", length=200, showvalue=False)
            poids_scale.bind("<ButtonRelease-1>", lambda event, index=i: self.adjust_sliders(event.widget.get(), index))
            self.sliders.append(poids_scale)
            self.sliders_vars.append(poids_var)
            poids_entry = tk.Entry(self.table.frame, textvariable=poids_var, width=5)
            self.table._create_table_entry(i + 1, 0, critere.get_nom())
            self.table._create_table_entry(i + 1, 1, poids_scale)
            self.table._create_table_entry(i + 1, 2, poids_entry)
    
    def adjust_sliders(self, value, index):
        value = int(round(float(value)))  # Convertir en entier pour IntVar
        total_sliders = len(self.sliders)
        remaining_sum = max(0, 100 - value)

        # Récupérer les valeurs actuelles des autres sliders
        current_values = [var.get() for i, var in enumerate(self.sliders_vars) if i != index]
        current_total = sum(current_values)

        # Si le slider sélectionné atteint 100, mettre les autres à 0
        if value >= 100:
            new_values = [0 if i != index else 100 for i in range(total_sliders)]
        elif current_total == 0:
            # Répartir uniformément si les autres sont à 0
            new_values = [remaining_sum // (total_sliders - 1) if i != index else value for i in range(total_sliders)]
        else:
            # Ajuster les autres sliders proportionnellement
            new_values = []
            for i, var in enumerate(self.sliders_vars):
                if i == index:
                    new_values.append(value)
                else:
                    new_value = int(round((var.get() / current_total) * remaining_sum))
                    new_values.append(new_value)

        # Corriger les petits écarts dus aux arrondis
        correction = 100 - sum(new_values)
        if correction != 0:
            for i in range(total_sliders):
                if i != index:
                    new_values[i] = max(0, min(100, new_values[i] + correction))
                    break

        # Mettre à jour tous les sliders
        for i, var in enumerate(self.sliders_vars):
            var.set(max(0, min(100, new_values[i])))
            self.criteres[i].set_poids(new_values[i])

class TableauGroupe(tk.Frame):
    def __init__(self, parent, page, partition:Partition, index, img_param_tk):
        super().__init__(parent)
        self.groupe = partition.get_groupes()[index]
        self.page=page
        self.partition = partition
        title_label = tk.Label(self, text=f"Groupe {index+1}", font=("Arial", 12, "bold"), 
                                    bg="#3D83B1", fg="white", width=15, height=2, anchor="center")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        nb_eleves_label = tk.Label(self, text=f"{len(self.groupe.get_eleves())}/{self.groupe.get_taille()}", font=("Arial", 12, "bold"), 
                                    bg="#3D83B1", fg="white", width=15, height=2, anchor="center")
        nb_eleves_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        # Créer le bouton avec l'image redimensionnée
        bouton_param_grp = tk.Button(self, image=img_param_tk, compound="right", anchor='e', command=lambda: self.pop_up_param_grp())
        bouton_param_grp.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        # Créer la liste des contraintes saisies
        nb_critere_avec_contraintes = len([v for v in partition.get_groupes()[index].get_contraintes().values() if len(v) > 0])
        if nb_critere_avec_contraintes > 0:
            font_height = tkf.Font(font=("Arial", 12)).metrics('linespace')
            contraintes_table = Table(self, self, height=(font_height+3)*(nb_critere_avec_contraintes+1))
            contraintes_table._create_table_headers(["Critère", "Valeurs"], [21]*2)
            contraintes_table.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
            for i, kv in enumerate(partition.get_groupes()[index].get_contraintes().items()):
                critere, valeurs = kv
                if(len(valeurs) == 0):
                    continue
                contraintes_table._create_table_entry(i+1, 0, critere.get_nom(), width=21)
                contraintes_table._create_table_entry(i+1, 1, ", ".join([str(critere.to_val(v)) for v in valeurs]), width=21)
        # Créer la table pour chaque groupe
        table = EleveTable(parent=self, controller=self, eleves=self.groupe.get_eleves(), criteres=self.partition.get_criteres())
        table.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        # Personnalisation des cellules du tableau
        for widget in table.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="white", fg="black", relief="solid", bd=1)
    def afficher_groupes(self):
        self.page.afficher_groupes()
    def pop_up_param_grp(self):
        from pages.parametresGroupe import ParametresGroupe
        popup = ParametresGroupe(self, self.partition, self.groupe)
        popup.grab_set()  # Pour forcer le focus sur la fenêtre pop-up