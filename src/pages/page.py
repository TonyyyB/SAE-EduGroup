import tkinter as tk
from constantes import *

class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = None
        # Création d'un canvas pour le dégradé
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        self.labels:dict[str,dict[str:float|str|tuple[str,int,str]]] = {
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

        for label_key, label in self.labels.items():
            try:
                # Assurez-vous que chaque clé nécessaire est présente
                x = width * label.get('x', 0.5)  # Valeur par défaut si clé manquante
                y = height * label.get('y', 0.1)  # Valeur par défaut si clé manquante
                text = label.get('text', "")
                font = label.get('font', ("Arial", 12))
                fill = label.get('fill', 'black')

                # Créer le texte sur le Canvas
                self.canvas.create_text(x, y, text=text, font=font, fill=fill,tags="labels")
            except Exception as e:
                print(f"Erreur lors de la création du texte '{label_key}': {e}")

    def on_resize(self, event):
        self.create_gradient()

    def clear_labels(self):
        self.labels.clear()
    
    def create_label(self, id, x, y, text, font=MOYENNE_POLICE, fill=None, background=None):
        if id in self.labels:
            raise Exception("Label already in list")
        
        # Ajoute le label à un dictionnaire avec un id unique
        self.labels[id] = {"x": x, "y": y, "text": text, "font": font, "fill": fill, "background": background}
    
    def change_text(self, id, text):
        if id in self.labels:
            self.labels[id]["text"] = text
            self.update_labels()  # Mettre à jour l'affichage des labels
        else:
            raise Exception("Label not found in list")
    
    def update_labels(self):
        """Supprime et redessine uniquement les labels sans toucher au dégradé."""
        self.canvas.delete("labels")  # Supprime tous les anciens labels

        width = self.winfo_width()
        height = self.winfo_height()

        for label_key, label in self.labels.items():
            try:
                x = width * label.get('x', 0.5)
                y = height * label.get('y', 0.1)
                text = label.get('text', "")
                font = label.get('font', ("Arial", 12))
                fill = label.get('fill', 'black')

                # Créer le texte avec un tag "labels" pour pouvoir l'effacer plus tard
                self.canvas.create_text(x, y, text=text, font=font, fill=fill, tags="labels")
            except Exception as e:
                print(f"Erreur lors de la mise à jour du texte '{label_key}': {e}")

import tkinter as tk

class Table(tk.Frame):
    def __init__(self, parent, controller, enable_scroll_x=False, enable_scroll_y=False, height=None, width=None):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, height=height, width=width) 
        if enable_scroll_x:
            self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.scrollbar_x.grid(row=1, column=0, sticky="ew")
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        if enable_scroll_y:
            self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scrollbar_y.grid(row=0, column=1, sticky="ns")
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.frame = tk.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame.columnconfigure(0, weight=1)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)  # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux (Scroll Up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux (Scroll Down)

        # Lier les événements de la molette au canvas
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        self.controller = controller

        # Configuration pour que le canvas s'ajuste automatiquement
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _bind_mousewheel(self, event):
        """Lie les événements de la molette au canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, event):
        """Délie les événements de la molette du canvas."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _create_table_headers(self, titre_colonnes, sizes=[]):
        for j, titre in enumerate(titre_colonnes):
            if len(sizes) > j and sizes[j] is not None:
                b = tk.Label(self.frame, text=titre, bg="lightgray", font=("Arial", 12), width=sizes[j])
            else:
                b = tk.Label(self.frame, text=titre, bg="lightgray", font=("Arial", 12))
            b.grid(row=0, column=j)

    def _create_table_entry(self, row, col, widget, width=15, color=None):
        """Crée une cellule dans le tableau."""
        if isinstance(widget, str) or isinstance(widget, int):
            widget = tk.Label(self.frame, text=widget, bg=color, font=("Arial", 12), width=width)
        widget.grid(row=row, column=col)

    def _on_mousewheel_windows(self, event):
        """Défilement sur Windows."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_mousewheel_linux(self, event):
        """Défilement sur Linux."""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

class EleveTable(Table):
    def __init__(self, parent, controller, eleves=None, criteres=None):
        super().__init__(parent, controller, enable_scroll_y=True, enable_scroll_x=True)
        self.controller = controller  # Controller pour gérer les événements (comme le clic sur un élève)

        # Si une liste d'élèves est fournie, créer le tableau à partir de ces données
        if eleves is not None and criteres is not None:
            self.create_table_from_eleves(eleves, criteres)

    def create_table_from_eleves(self, eleves, criteres):
        """
        Crée un tableau basé sur une liste d'élèves et des critères.
        Affiche le nom, prénom, ID, et les notes pour chaque critère.
        Chaque cellule du tableau est un label cliquable pour les interactions.
        """
        criteres_tries = sorted(criteres, key=lambda c: c.get_poids(), reverse=True)
        # Définir les titres de colonnes : Prénom, Nom + critères
        self.titre_colonnes = ['Prénom', 'Nom', 'Genre'] + [c.get_nom() for c in criteres_tries]

        # Créer les titres des colonnes
        self._create_table_headers(self.titre_colonnes)

        # Remplir les lignes avec les données des élèves
        for i, eleve in enumerate(eleves):
            # Colonnes fixes : prénom, nom, genre
            self._create_clickable_table_entry(i + 1, 0, eleve.prenom, eleve)  # Ajout du bind sur prénom
            self._create_clickable_table_entry(i + 1, 1, eleve.nom, eleve)
            self._create_clickable_table_entry(i + 1, 2, eleve.genre, eleve)# Ajout du bind sur nom

            # Colonnes dynamiques : notes pour chaque critère
            for j, critere in enumerate(criteres_tries):
                note = eleve.get_critere(critere)
                self._create_clickable_table_entry(i + 1, j + 3, note, eleve)  # Ajout du bind sur chaque note

    def _create_clickable_table_entry(self, row, col, text, eleve):
        """
        Crée une cellule cliquable dans la table. Chaque cellule est un `Label` qui réagit aux clics.
        """
        # Créer un label pour chaque cellule
        label = tk.Label(self.frame, text=text, bg="white", fg="black", width=12, height=2, anchor="w")
<<<<<<< Updated upstream
        label.grid(row=row, column=col, padx=0, pady=0, sticky="we")
=======
        label.grid(row=row, column=col, padx=0, pady=0, sticky="EW")
>>>>>>> Stashed changes
        
        # Associer l'objet élève au label pour permettre de l'identifier lors du clic
        label.eleve = eleve

        # Lier l'événement de clic sur le label pour la gestion des interactions
        label.bind("<Button-1>", self.on_eleve_click)

    def on_eleve_click(self, event):
        """
        Gère le clic sur une cellule de la table. L'événement récupère l'élève associé.
        """
        widget = event.widget
        eleve = getattr(widget, "eleve", None)  # Récupérer l'objet Eleve associé au widget

        if eleve is None:
            print("Erreur : aucun élève trouvé pour ce widget.")
            return

        # Appel de la méthode de sélection d'élève dans le controller principal (TableauGroupe par ex.)
        self.controller.on_eleve_click(event)  # Passer l'événement à une méthode dans le controller

        # Debug pour afficher l'élève sélectionné
        print(f"Élève sélectionné : {eleve.get_nom()}")
