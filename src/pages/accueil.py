import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

class PageAccueil(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = None

        # Création d'un canvas pour le dégradé
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Dessiner le dégradé initial
        self.create_gradient()

        # Titre "EduGroup" en haut à gauche
        self.title_text = self.canvas.create_text(
            50, 30, text="EduGroup", font=("Helvetica", 32, "bold"), fill='white', anchor='nw'
        )

        # Instruction centrée
        self.instruction_text = self.canvas.create_text(
            400, 150, text="Choisir le chemin du fichier :", font=("Helvetica", 20, "bold"), fill='white', anchor='center'
        )

        # Zone de dépôt de fichier centrée avec tkinterdnd2 + fonctionnalité de bouton
        self.frame = tk.Frame(self, bg='white', padx=10, pady=12, relief=tk.RIDGE, bd=5)
        self.frame.place(relx=0.5, rely=0.4, anchor='center', relwidth=0.6, relheight=0.2)

        # Initialiser la fonctionnalité DnD pour la fenêtre Tkinter
        self.dnd_frame = self.frame
        self.dnd_frame.drop_target_register(DND_FILES)
        self.dnd_frame.dnd_bind('<<Drop>>', self.on_file_drop)

        # Lier la zone de dépôt à un clic pour ouvrir l'explorateur de fichiers
        self.frame.bind("<Button-1>", self.open_file_explorer)

        # Label dans la zone de dépôt/bouton
        self.drop_label = tk.Label(self.frame, text="Déposer le fichier ici ou cliquez pour choisir", bg='white', font=("Helvetica", 14))
        self.drop_label.pack(expand=True)

        # Bouton pour supprimer le fichier sélectionné
        self.clear_button = tk.Button(self.frame, text="❌", command=self.clear_file, bg='red', fg='white', font=("Helvetica", 12), width=2)
        self.clear_button.pack(side='right')

        # Boutons en bas de la fenêtre
        self.import_button = tk.Button(self, text="Importer des paramètres", command=self.import_params, bg='#3498DB', fg='white', font=("Helvetica", 12))
        self.import_button.place(relx=0.25, rely=0.8, anchor='center', relwidth=0.25, relheight=0.08)

        self.create_button = tk.Button(self, text="Démarrer la création de groupe", command=self.go_to_next_page, bg='#3498DB', fg='white', font=("Helvetica", 12))
        self.create_button.place(relx=0.75, rely=0.8, anchor='center', relwidth=0.25, relheight=0.08)

        # Lier l'événement de redimensionnement à la fonction de mise à jour du dégradé
        self.bind("<Configure>", self.on_resize)

    def create_gradient(self):
        # Dessine un dégradé du bleu vers le noir
        self.canvas.delete("all")
        start_color = (45, 98, 160)
        end_color = (1, 31, 67)

        height = self.winfo_height()
        width = self.winfo_width()

        for i in range(height):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / height))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / height))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / height))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

        self.title_text = self.canvas.create_text(
            50, 30, text="EduGroup", font=("Helvetica", 32, "bold"), fill='white', anchor='nw'
        )
        self.instruction_text = self.canvas.create_text(
            width / 2, 150, text="Choisir le chemin du fichier :", font=("Helvetica", 20, "bold"), fill='white', anchor='center'
        )

    def on_resize(self, event):
        self.create_gradient()

    def on_file_drop(self, event):
        # Nettoyer le chemin du fichier
        self.file_path = event.data.strip('{}')

        # Vérifier si le fichier est un CSV
        if self.file_path.endswith(".csv"):
            self.drop_label.config(text=f"Fichier ajouté : {self.file_path.split('/')[-1]}")
        else:
            # Alerte si ce n'est pas un fichier CSV
            self.file_path = None
            messagebox.showerror("Erreur", "Veuillez déposer uniquement des fichiers CSV.")
            self.drop_label.config(text="Déposer le fichier ici ou cliquez pour choisir")

    def open_file_explorer(self, event=None):
        # Ouvre l'explorateur de fichiers pour sélectionner un fichier CSV
        self.file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if self.file_path:
            if self.file_path.endswith(".csv"):
                self.drop_label.config(text=f"Fichier ajouté : {self.file_path.split('/')[-1]}")
            else:
                # Alerte si ce n'est pas un fichier CSV
                self.file_path = None
                messagebox.showerror("Erreur", "Veuillez sélectionner uniquement des fichiers CSV.")
                self.drop_label.config(text="Déposer le fichier ici ou cliquez pour choisir")

    def clear_file(self):
        self.file_path = None
        self.drop_label.config(text="Déposer le fichier ici ou cliquez pour choisir")

    def import_params(self):
        pass

    def go_to_next_page(self):
        if not self.file_path:
            messagebox.showwarning("Avertissement", "Veuillez ajouter un fichier avant de continuer.")
            return
        messagebox.showinfo("Info", "Passage à la page suivante")