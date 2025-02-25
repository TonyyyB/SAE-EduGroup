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
                self.canvas.create_text(x, y, text=text, font=font, fill=fill)
            except Exception as e:
                print(f"Erreur lors de la création du texte '{label_key}': {e}")



    def on_resize(self, event):
        self.create_gradient()
        
    def go_to_next_page(self):
        pass

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
        else:
            raise Exception("Label not found in list")
class Table(tk.Frame):
    def __init__(self, parent, controller, eleves=None, criteres=None):
        super().__init__(parent)

        self.canvas = tk.Canvas(self)
        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.frame = tk.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.controller = controller

        # Si une liste d'élèves est fournie, créer le tableau à partir de ces données
        if eleves is not None and criteres is not None:
            self.create_table_from_eleves(eleves, criteres)

        # Configuration pour que le canvas s'ajuste automatiquement
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_table_from_eleves(self, eleves, criteres):
        """
        Crée un tableau basé sur une liste d'élèves et des critères.
        Affiche le nom, prénom, ID, et les notes pour chaque critère.
        """
        # Définir les titres de colonnes : Prénom, Nom, ID + critères
        self.titre_colonnes = ['Prénom', 'Nom', 'ID'] + [c.get_nom() for c in criteres]

        # Créer les titres des colonnes
        for j, titre in enumerate(self.titre_colonnes):
            b = tk.Label(self.frame, text=titre, bg="lightgray", font=("Arial", 12), width=15)
            b.grid(row=0, column=j)

        # Remplir les lignes avec les données des élèves
        for i, eleve in enumerate(eleves):
            # Colonnes fixes : prénom, nom, ID
            self._create_table_entry(i + 1, 0, eleve.prenom)
            self._create_table_entry(i + 1, 1, eleve.nom)
            self._create_table_entry(i + 1, 2, eleve.num_etudiant)

            # Colonnes dynamiques : notes pour chaque critère
            for j, critere in enumerate(criteres):
                note = eleve.get_critere(critere)
                self._create_table_entry(i + 1, j + 3, note)

    def _create_table_entry(self, row, col, text):
        """Crée une cellule dans le tableau."""
        entry = tk.Label(self.frame, text=text, bg="white", font=("Arial", 12), width=15)
        entry.grid(row=row, column=col)

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
        # Si une liste d'élèves est fournie, créer le tableau à partir de ces données
        if eleves is not None and criteres is not None:
            self.create_table_from_eleves(eleves, criteres)
    def create_table_from_eleves(self, eleves, criteres):
        """
        Crée un tableau basé sur une liste d'élèves et des critères.
        Affiche le nom, prénom, ID, et les notes pour chaque critère.
        """
        # Définir les titres de colonnes : Prénom, Nom, ID + critères
        self.titre_colonnes = ['Prénom', 'Nom', 'ID'] + [c.get_nom() for c in criteres]

        # Créer les titres des colonnes
        self._create_table_headers(self.titre_colonnes, [10]*len(self.titre_colonnes))

        # Remplir les lignes avec les données des élèves
        for i, eleve in enumerate(eleves):
            # Colonnes fixes : prénom, nom, ID
            self._create_table_entry(i + 1, 0, eleve.prenom)
            self._create_table_entry(i + 1, 1, eleve.nom)
            self._create_table_entry(i + 1, 2, eleve.num_etudiant)

            # Colonnes dynamiques : notes pour chaque critère
            for j, critere in enumerate(criteres):
                note = critere.to_val(eleve.get_critere(critere))
                self._create_table_entry(i + 1, j + 3, note)

