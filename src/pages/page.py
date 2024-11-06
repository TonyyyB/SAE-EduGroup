import tkinter as tk
from tkinter import ttk, font
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
        t = Table(self,controller,4,4,["Nom","Type","Minimal","Maximal"], titres_en_haut=True, desactiver_toutes_valeures=True)
        t.place(relx=0.5, rely=0.5,anchor="center",relwidth=0.5, relheight=0.5)
        t.fill_row(1, ["Salut","Comment","Ca","Va"])
        t.fill_row(2,["Zero","Zero","Ensuite toi","Eeeeeet"])

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

class Table(ttk.Frame):
    def __init__(self, parent, controller, nb_lignes, nb_colonnes, titres, titres_en_haut=True, desactiver_toutes_valeures=False):
        super().__init__(parent)
        if titres_en_haut:
            if nb_colonnes != len(titres):
                raise Exception("Nombre de colonnes incompatible avec le nombre de titres de colonnes")
        else:
            if nb_lignes != len(titres):
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
        self.frame = ttk.Frame(self.canvas)
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Ajouter la frame dans le canvas
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Disposition du canvas et de la scrollbar dans la grille
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")  # Placer la scrollbar horizontale en bas

        self.controller = controller
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.titres = titres
        self.titres_en_haut = titres_en_haut
        self.desactiver_toutes_valeures = desactiver_toutes_valeures
        self.police_titre = font.Font(family=TITRE_COLONNE_POLICE[0],size=TITRE_COLONNE_POLICE[1],weight=TITRE_COLONNE_POLICE[2])
        self.police_valeure = font.Font(family=VALEUR_LIGNE_POLICE[0],size=VALEUR_LIGNE_POLICE[1],weight=VALEUR_LIGNE_POLICE[2])

        # Création de la table
        self.create_table()

        # Configuration pour que le canvas s'ajuste automatiquement
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def _bind_mousewheel(self, event):
        # Liaison de la molette de la souris pour différents systèmes d'exploitation
        if event.widget == self.canvas:
            if self.winfo_toplevel().tk.call('tk', 'windowingsystem') == 'win32':
                self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
            else:
                # Pour macOS et Linux
                self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
                self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, event):
        # Supprimer les liaisons de la molette de la souris
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel_windows(self, event):
        # Gestion du scroll pour Windows/macOS
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_mousewheel_linux(self, event):
        # Gestion du scroll pour Linux
        if event.num == 4:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            self.canvas.yview_scroll(1, "units")
        
    def create_table(self):
        # Création des titres
        for j, titre in enumerate(self.titres):
            b = tk.Entry(self.frame, font=self.police_titre, disabledbackground="lightgrey", disabledforeground="black", width=10)
            b.insert(0, titre)
            b.configure(state="disabled")
            b.grid(row=0, column=j) if self.titres_en_haut else b.grid(row=j, column=0)
        
        # Création des valeurs
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                b = tk.Entry(self.frame, font=self.police_valeure, foreground="black",width=10)
                b.insert(0, TABLE_VALEUR_DEFAUT)
                b.grid(row=i+1, column=j) if self.titres_en_haut else b.grid(row=i, column=j+1)
                b.configure(state="disabled" if self.desactiver_toutes_valeures else "normal")

        # Ajustement des largeurs des colonnes
        self.update_largeur_colonnes()

    def update_largeur_colonnes(self):
        # Calcul des largeurs maximales pour chaque colonne en pixels
        largeurs_colonnes_pixels = []
        
        for col_index in range(self.nb_colonnes):
            largeur_max_colonne = 0
            # Itérer sur chaque cellule de la colonne (titres + valeurs)
            for entry in self.frame.grid_slaves(column=col_index):
                police = self.police_titre if entry.grid_info()['row'] == 0 else self.police_valeure
                largeur_valeur = police.measure(entry.get())
                largeur_max_colonne = max(largeur_max_colonne, largeur_valeur)

            # Enregistrer la largeur max pour cette colonne en pixels
            largeurs_colonnes_pixels.append(largeur_max_colonne)

        # Conversion de la largeur en pixels vers caractères moyens pour l'argument `width`
        largeur_caractere_moyen = self.police_valeure.measure("0")
        largeurs_colonnes = [int(px / largeur_caractere_moyen) for px in largeurs_colonnes_pixels]
        
        # Appliquer les largeurs calculées aux entrées
        for col_index, largeur in enumerate(largeurs_colonnes):
            for entry in self.frame.grid_slaves(column=col_index):
                entry.configure(width=largeur+1)

    def get_entry(self, ligne, colonne):
        return self.frame.grid_slaves(row=ligne, column=colonne)[0]
    
    def fill_row(self, ligne, donnees):
        if len(donnees) != self.nb_colonnes:
            raise Exception("Pas le même nombre de données que de colonnes")
        state = "normal"
        for col_index, entry in enumerate(self.frame.grid_slaves(row=ligne+1)):
            state = entry["state"]
            entry["state"] = "normal"
            entry.delete(0, tk.END)
            entry.insert(0,donnees[entry.grid_info()["column"]])
            entry["state"] = state
        self.update_largeur_colonnes()

class Boutton(tk.Button):
    def __init__(self, parent, text, command=None, state=tk.NORMAL):
        super().__init__(parent, text=text, command=command, bg="#3498DB", fg="white", font=MOYENNE_POLICE, state=state)