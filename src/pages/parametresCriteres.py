import tkinter as tk
from tkinter import messagebox

class ParametresCriteres(tk.Toplevel):
    def __init__(self, parent, criteres):
        super().__init__(parent)
        self.title("Paramétrage des critères")
        self.geometry("1000x400")
        
        # Création d'un Canvas pour le dégradé
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # Dessiner un dégradé
        self.create_gradient()
        
        # Frame pour les éléments de la fenêtre
        self.frame = tk.Frame(self.canvas, bg="#4C8DAB")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Label principal
        self.label = tk.Label(self.frame, text="Paramétrage des critères", font=("Arial", 30, "bold"), bg="#4C8DAB", fg="white")
        self.label.pack(pady=20)

        # Ajout du tableau de critères
        self.table_frame = tk.Frame(self.frame, bg="#4C8DAB")
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.entetes = ["Nom des critères", "Poids", "Regrouper", "Valeur Minimale", "Valeur Maximale", "Types"]
        for col_num, entete in enumerate(self.entetes):
            label = tk.Label(self.table_frame, text=entete, font=("Arial", 12, "bold"), bg="#4C8DAB", fg="white", width=15)
            label.grid(row=0, column=col_num, padx=5, pady=5)

        # Champs de saisie pour les critères
        self.entries = []
        for i, critere in enumerate(criteres):
            nom_critere = critere.get('nom', '')
            poids = critere.get('poids', '')
            regrouper = critere.get('regrouper', '')
            valeur_min = critere.get('valeur_min', '')
            valeur_max = critere.get('valeur_max', '')
            type_critere = critere.get('type', '')

            row = []
            row.append(tk.Label(self.table_frame, text=nom_critere, width=15, anchor="w", bg="#4C8DAB", fg="white"))
            row.append(tk.Entry(self.table_frame, width=10, bg="#ffffff"))
            row.append(tk.Entry(self.table_frame, width=10, bg="#ffffff"))
            row.append(tk.Entry(self.table_frame, width=10, bg="#ffffff"))
            row.append(tk.Entry(self.table_frame, width=10, bg="#ffffff"))
            row.append(tk.Entry(self.table_frame, width=10, bg="#ffffff"))

            for col_num, widget in enumerate(row):
                widget.grid(row=i + 1, column=col_num, padx=5, pady=5)

            self.entries.append(row)

        # Boutons "Annuler" et "Valider"
        self.bouton_annuler = tk.Button(self.frame, text="Annuler", command=self.destroy, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_annuler.pack(side="left", padx=30, pady=20)

        self.bouton_valider = tk.Button(self.frame, text="Valider", command=self.sauvegarder_criteres, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_valider.pack(side="right", padx=30, pady=20)

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
        # Récupérer les données des entrées
        criteres_sauves = {}
        for i, entry_row in enumerate(self.entries):
            criteres_sauves[i] = {
                'nom': entry_row[0].cget("text"),
                'poids': entry_row[1].get(),
                'regrouper': entry_row[2].get(),
                'valeur_min': entry_row[3].get(),
                'valeur_max': entry_row[4].get(),
                'type': entry_row[5].get()
            }

        # Affichage des critères sauvegardés
        print("Critères sauvegardés:", criteres_sauves)
        messagebox.showinfo("Sauvegarde", "Les critères ont été sauvegardés avec succès !")
        self.destroy()

# Exemple d'utilisation avec quelques critères fictifs
criteres = [
    {'nom': 'niveau_francais', 'poids': '10', 'regrouper': 'Oui', 'valeur_min': '1', 'valeur_max': '5', 'type': 'Numérique'},
    {'nom': 'niveau_maths', 'poids': '5', 'regrouper': 'Non', 'valeur_min': 'A', 'valeur_max': 'F', 'type': 'Numérique'},
    {'nom': 'ecole_origine', 'poids': '2', 'regrouper': 'Non', 'valeur_min': '', 'valeur_max': '', 'type': 'Catégorique'},
    {'nom': 'handicap', 'poids': '1', 'regrouper': 'Non', 'valeur_min': '', 'valeur_max': '', 'type': 'Booléen'}
]

root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale
popup = ParametresCriteres(root, criteres)
popup.mainloop()