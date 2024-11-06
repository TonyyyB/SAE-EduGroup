import tkinter as tk
from tkinter import filedialog, messagebox
from constantes import *

class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = None
        # Création d'un canvas pour le dégradé
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        self.labels = {
            "title" : {"x":0.1, "y":0.1, "text":"EduGroup", "font":GRANDE_POLICE, "fill":"white"}
        }

        # Dessiner le dégradé initial
        self.create_gradient()

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

        for label in self.labels.values():
            self.canvas.create_text(
                width*label["x"],
                height*label["y"],
                text=label["text"],
                font=label["font"],
                fill=label["fill"]
            )

    def on_resize(self, event):
        self.create_gradient()

    def go_to_next_page(self):
        pass
    
    def create_label(self, id, x, y, text, font=MOYENNE_POLICE, fill="white"):
        if id in self.labels:
            raise Exception("Label already in list")
        self.labels[id] = {"x":x, "y":y, "text":text, "font":font, "fill":fill}

class Table(tk.Frame):
    def __init__(self, parent, controller, nb_lignes, nb_colonnes, titre_colonnes):
        super().__init__(parent)
        if nb_colonnes != len(titre_colonnes):
            raise Exception("Nombre de colonnes incompatible avec le nombre de titres de colonnes")

        # Créer un canvas pour scroller la frame contenant la table
        self.canvas = tk.Canvas(self)
        
        # Ajouter une scrollbar verticale
        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
        # Ajouter une scrollbar horizontale
        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # Frame qui contiendra la table
        self.frame = tk.Frame(self.canvas)
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Ajouter la frame dans le canvas
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Disposition du canvas et des scrollbars dans la grille
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")  # Placer la scrollbar horizontale en bas

        self.controller = controller
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.titre_colonnes = titre_colonnes

        # Création de la table
        self.create_table()

        # Configuration pour que le canvas s'ajuste automatiquement
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
    def create_table(self):
        for j in range(len(self.titre_colonnes)):
            b = tk.Entry(self.frame, disabledbackground="lightgray", disabledforeground="black", font=("Arial", 12), width=20)
            b.insert(0, self.titre_colonnes[j])
            b.configure(state="disabled")
            b.grid(row=0, column=j)
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                b = tk.Entry(self.frame, font=("Arial", 12), foreground="black")
                b.insert(0, f"bite {i} {j}")
                b.grid(row=i+1, column=j)
    
    def get_entry(self, ligne, colonne):
        return self.grid_slaves(row=ligne, column=colonne)[0]