import tkinter as tk
from tkinter import messagebox

class ParametresGroupe(tk.Toplevel):
    def __init__(self, parent, eleves_restants, criteres):
        super().__init__(parent)
        self.title("Paramétrage des groupes")
        self.geometry("1000x600")
        self.resizable(False,False)
        self.configure(bg="#2D62A0")
        
        self.eleves_restants = eleves_restants  # Le nombre d'élèves restants
        self.criteres = criteres  # Liste des critères à afficher
        
        # Nombre d'élèves dans le groupe (Input box avec validation)
        self.label_nb_eleve = tk.Label(self, text="Nombre d'élève\ndans le groupe", font=("Arial", 14), bg="#4C8DAB", fg="white", width=18, height=3)
        self.label_nb_eleve.place(x=50, y=100)

        self.eleves_dans_grp_var = tk.StringVar(value="1")
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
        valeurs_possibles=["1","2","3"]
        self.criteres_values = dict()
        for critere in self.criteres:
            self.criteres_values[critere]=valeurs_possibles

        self.checkbox_vars = {}  # Stocke les variables des checkboxes pour chaque critère

        for row_num, (critere, valeurs) in enumerate(self.criteres_values.items()):
            label = tk.Label(self.table_frame, text=critere, font=("Arial", 12), bg="white", fg="black", width=15)
            label.grid(row=row_num+1, column=0, padx=5, pady=5)
            
            checkbox_frame = tk.Frame(self.table_frame, bg="white")
            checkbox_frame.grid(row=row_num+1, column=1, padx=5, pady=5)
            
            # Créer une variable pour chaque valeur possible du critère
            self.checkbox_vars[critere] = []
            for valeur in valeurs:
                var = tk.BooleanVar()  # Variable pour chaque checkbox
                checkbox = tk.Checkbutton(checkbox_frame, text=valeur, variable=var, bg="white")
                checkbox.pack(side="left", padx=5)
                self.checkbox_vars[critere].append(var)

        # Boutons Annuler et Valider
        self.bouton_annuler = tk.Button(self, text="Annuler", command=self.destroy, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_annuler.place(x=50, y=500)

        self.bouton_valider = tk.Button(self, text="Valider", command=self.sauvegarder_criteres, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_valider.place(x=800, y=500)

    def valider_nb_eleve(self, event):
        # Valide que le nombre d'élèves dans le groupe est inférieur ou égal aux élèves restants
        try:
            nb_eleve = int(self.eleves_dans_grp_var.get())
            if nb_eleve > self.eleves_restants:
                messagebox.showerror("Erreur", f"Le nombre d'élèves ne peut pas dépasser {self.eleves_restants}")
                self.eleves_dans_grp_var.set(str(self.eleves_restants))
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide")
            self.eleves_dans_grp_var.set("1")

    def sauvegarder_criteres(self):
        # Récupérer les valeurs cochées pour chaque critère
        criteres_selectionnes = {}
        for critere, vars_liste in self.checkbox_vars.items():
            criteres_selectionnes[critere] = [var.get() for var in vars_liste]
        
        messagebox.showinfo("Sauvegarde", "Les critères ont été sauvegardés avec succès !")
        self.destroy()

# Fenêtre principale
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale