import tkinter as tk
from tkinter import messagebox

class ParametresCriteres(tk.Toplevel):
    def __init__(self, parent, criteres):
        super().__init__(parent)
        self.title("Paramétrage des critères")
        self.geometry("1000x400")
        self.resizable(False,False)
        self.criteres = criteres  # Liste de critères fournie directement
        
        # Création d'un Canvas pour le dégradé
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # Mise à jour de la taille pour le dégradé
        self.update_idletasks()
        
        # Dessiner un dégradé
        self.create_gradient()
        
        # Frame pour les éléments de la fenêtre
        self.frame = tk.Frame(self.canvas)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Label principal
        self.label = tk.Label(self.frame, text="Paramétrage des critères", font=("Arial", 30, "bold"), bg="#4C8DAB", fg="white")
        self.label.pack(pady=20)

        # Ajout du tableau de critères
        self.table_frame = tk.Frame(self.frame)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.entetes = ["Nom des critères", "Poids", "Répartis", "Valeur Minimale", "Valeur Maximale", "Types"]

        self.bouton_annuler = tk.Button(self.frame, text="Annuler", command=self.destroy, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_annuler.pack(side="left", padx=30, pady=20)

        self.bouton_valider = tk.Button(self.frame, text="Valider", command=self.sauvegarder_criteres, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_valider.pack(side="right", padx=30, pady=20)
        
        # Afficher le tableau et le dégradé
        self.creerTableau()

    def creerTableau(self):
        self.entries_var = dict()
        # Ajouter les en-têtes de colonnes
        for col_num, entete in enumerate(self.entetes):
            label = tk.Label(self.table_frame, text=entete, font=("Arial", 12, "bold"), bg="#4C8DAB", fg="white", width=15)
            label.grid(row=0, column=col_num, padx=5, pady=5)

        # Ajouter les lignes de critères à partir de self.criteres
        for row_num, critere in enumerate(self.criteres):
            # Critère dans la première colonne
            label = tk.Label(self.table_frame, text=critere.get_nom(), font=("Arial", 12, "bold"), bg="white", fg="black", width=15)
            label.grid(row=row_num+1, column=0, padx=5, pady=5)  # Les critères sont affichés dans la première colonne

            # Valeurs:
            # Poids
            poids_var = tk.IntVar(value=critere.get_poids())
            poids = tk.Entry(self.table_frame, textvariable=poids_var, font=("Arial", 12), bg="white", fg="black", width=15)
            poids.grid(row=row_num+1, column=1, padx=5, pady=5)

            # Repartis
            repartis_var = tk.BooleanVar(value=critere.est_reparti())
            repartis = tk.Checkbutton(self.table_frame, variable=repartis_var, text="")
            repartis.grid(row=row_num+1, column=2, padx=5, pady=5)

            # Valeurs minimales et maximales
            minimum = tk.Label(self.table_frame, text=critere.get_valeur_min(), font=("Arial", 12), bg="white", fg="black", width=15)
            maximum = tk.Label(self.table_frame, text=critere.get_valeur_max(), font=("Arial", 12), bg="white", fg="black", width=15)
            minimum.grid(row=row_num+1, column=3, padx=5, pady=5)
            maximum.grid(row=row_num+1, column=4, padx=5, pady=5)

            # Types de critères
            types = tk.Label(self.table_frame, text="", font=("Arial", 12), bg="white", fg="black", width=15)
            types.grid(row=row_num+1, column=5, padx=5, pady=5)  # Les types des critères sont affichés dans la sixième colonne

            self.entries_var[critere] = [poids_var, repartis_var]

    def create_gradient(self):
        # Dessine un dégradé du bleu vers le noir
        self.canvas.delete("all")
        start_color = (45, 98, 160)  # Bleu
        end_color = (1, 31, 67)  # Noir

        height = self.winfo_height()
        width = self.winfo_width()

        # Dessine le dégradé sur le Canvas
        for i in range(height):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / height))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / height))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / height))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def sauvegarder_criteres(self):
        # Valider la saisie des poids (int)
        for critere, entries in self.entries_var.items():
            poids_var, _ = entries
            try:
                poids = poids_var.get()
                if not isinstance(poids, int):
                    raise ValueError("Le poids doit être un entier.")
            except ValueError as e:
                messagebox.showerror("Erreur: vous devez saisir un nombre pour le poids du critere " + critere.get_nom())
                return
            except tk.t as e:
                messagebox.showerror("Erreur: vous devez saisir un nombre pour le poids du critere " + critere.get_nom())
                return

        # Valider la saisie des valeurs des champs (int ou float)
        # Récupérer les valeurs des champs
        for critere, entries in self.entries_var.items():
            poids_var, repartis_var = entries
            critere.set_poids(poids_var.get())
            critere.set_repratis(repartis_var.get())

        # Afficher un message de confirmation et fermer la fenêtre
        messagebox.showinfo("Sauvegarde", "Les critères ont été sauvegardés avec succès !")
        self.destroy()

root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale