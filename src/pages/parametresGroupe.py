import tkinter as tk
from tkinter import messagebox
from modele.partition import Partition
from modele.groupe import Groupe

class ParametresGroupe(tk.Toplevel):
    def __init__(self, parent, partition: Partition, groupe: Groupe):
        super().__init__(parent)
        self.parent = parent
        self.partition = partition
        self.groupe = groupe
        self.title("Paramétrage des groupes")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.configure(bg="#2D62A0")
        
        self.titre_groupe = tk.Label(self, text="Groupe " + str(self.partition.groupes.index(groupe)+1), font=("Arial", 45), bg="#4C8DAB", fg="white", width=10)
        self.titre_groupe.place(x=325, y=5)
        
        print(self.partition.groupes.index(groupe))
        # Nombre d'élèves dans le groupe (Input box avec validation)
        self.label_nb_eleve = tk.Label(self, text="Nombre d'élève\ndans le groupe", font=("Arial", 14), bg="#4C8DAB", fg="white", width=18, height=3)
        self.label_nb_eleve.place(x=50, y=100)

        self.eleves_dans_grp_var = tk.StringVar(value=str(groupe.get_taille()))
        self.entry_nb_eleve = tk.Entry(self, textvariable=self.eleves_dans_grp_var, font=("Arial", 24), width=5, justify="center")
        self.entry_nb_eleve.place(x=100, y=180)

        # Vérifier que le nombre d'élèves dans le groupe ne dépasse pas les élèves restants
        self.entry_nb_eleve.bind('<FocusOut>', self.valider_nb_eleve)

        # Frame contenant la table des critères
        self.table_frame = tk.Frame(self, bg="#2D62A0")
        self.table_frame.place(x=300, y=120)

        # En-têtes des critères
        self.label_nom_critere = tk.Label(self.table_frame, text="Nom du critère", font=("Arial", 12, "bold"), bg="#4C8DAB", fg="white", width=15)
        self.label_nom_critere.grid(row=0, column=0, padx=5, pady=5)

        self.label_valeur_possible = tk.Label(self.table_frame, text="Valeurs possibles", font=("Arial", 12, "bold"), bg="#4C8DAB", fg="white", width=30)
        self.label_valeur_possible.grid(row=0, column=1, padx=5, pady=5)

        # Critères et valeurs possibles avec Checkboxes dynamiques
        self.criteres_values = dict()
        for critere in self.partition.get_criteres():
            self.criteres_values[critere]=sorted(list(critere.get_valeurs()))

        self.checkbox_vars = {}  # Stocke les variables des checkboxes pour chaque critère


        for row_num, (critere, valeurs) in enumerate(self.criteres_values.items()):
            valeurs_possibles_actuels = groupe.get_contrainte(critere)
            label = tk.Label(self.table_frame, text=critere.get_nom(), font=("Arial", 12), bg="white", fg="black", width=15)
            label.grid(row=row_num+1, column=0, padx=5, pady=5)
            
            checkbox_frame = tk.Frame(self.table_frame, bg="white")
            checkbox_frame.grid(row=row_num+1, column=1, padx=5, pady=5)
            
            # Créer une variable pour chaque valeur possible du critère
            self.checkbox_vars[critere] = []
            for i, valeur in enumerate(valeurs):
                var = tk.BooleanVar()  # Variable pour chaque checkbox
                if valeurs_possibles_actuels is not None:
                    var.set(valeur in valeurs_possibles_actuels)
                checkbox = tk.Checkbutton(checkbox_frame, text=str(valeur), variable=var, bg="white")
                checkbox.pack(side="left", padx=5)
                self.checkbox_vars[critere].append((valeur,var))

        # Boutons Annuler et Valider
        self.bouton_annuler = tk.Button(self, text="Annuler", command=self.destroy, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_annuler.place(x=50, y=500)

        self.bouton_valider = tk.Button(self, text="Valider", command=self.sauvegarder_criteres, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_valider.place(x=800, y=500)

    def valider_nb_eleve(self, event):
        # Valide que le nombre d'élèves dans le groupe est inférieur ou égal aux élèves restants
        try:
            nb_eleve = int(self.eleves_dans_grp_var.get())
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide")
            self.eleves_dans_grp_var.set("1")

    def sauvegarder_criteres(self):
        # Récupérer les valeurs cochées pour chaque critère
        for critere, vars_list in self.checkbox_vars.items():
            criteres_selectionnes = set()
            for val, var in vars_list:
                if var.get():
                    criteres_selectionnes.add(val)
            self.groupe.set_contrainte(critere, criteres_selectionnes)
        newTaille = int(self.entry_nb_eleve.get())
        if newTaille != self.groupe.get_taille():
            oldTaille = self.groupe.get_taille()
            try:
                self.groupe.changer_taille(newTaille)
                self.partition.adapter_taille()
            except ValueError:
                self.groupe.changer_taille(oldTaille)
                messagebox.showerror("Erreur", f"Impossible de changer la taille du groupe de {oldTaille} à {newTaille}.")
                return
        self.destroy()
        self.update()
        self.parent.afficher_groupes()

# Fenêtre principale
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale