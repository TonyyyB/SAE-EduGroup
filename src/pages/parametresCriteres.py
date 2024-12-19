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

        self.entetes = ["Nom des critères", "Poids", "Regrouper", "Valeur Minimale", "Valeur Maximale", "Types"]

        self.bouton_annuler = tk.Button(self.frame, text="Annuler", command=self.destroy, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_annuler.pack(side="left", padx=30, pady=20)

        self.bouton_valider = tk.Button(self.frame, text="Valider", command=self.sauvegarder_criteres, bg="#F0F4F7", font=("Arial", 14), width=12)
        self.bouton_valider.pack(side="right", padx=30, pady=20)
        
        # Afficher le tableau et le dégradé
        self.creerTableau()

    def creerTableau(self):
        # Ajouter les en-têtes de colonnes
        for col_num, entete in enumerate(self.entetes):
            label = tk.Label(self.table_frame, text=entete, font=("Arial", 12, "bold"), bg="#4C8DAB", fg="white", width=15)
            label.grid(row=0, column=col_num, padx=5, pady=5)

        # Ajouter les lignes de critères à partir de self.criteres
        for row_num, critere in enumerate(self.criteres):
            # Critère dans la première colonne
            label = tk.Label(self.table_frame, text=critere, font=("Arial", 12, "bold"), bg="white", fg="black", width=15)
            label.grid(row=row_num+1, column=0, padx=5, pady=5)  # Les critères sont affichés dans la première colonne

            # Exemple pour les autres colonnes avec des valeurs par défaut (Vous pouvez personnaliser)
            for col_num in range(1, len(self.entetes)):
                label = tk.Label(self.table_frame, text="Valeur", font=("Arial", 12), bg="white", fg="black", width=15)
                label.grid(row=row_num+1, column=col_num, padx=5, pady=5)

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
        messagebox.showinfo("Sauvegarde", "Les critères ont été sauvegardés avec succès !")
        self.destroy()

root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale