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
                width * label["x"],
                height * label["y"],
                text=label["text"],
                font=label["font"],
                fill=label["fill"]
            )


    def on_resize(self, event):
        self.create_gradient()

    def go_to_next_page(self):
        pass
    
    def create_label(self, id, x, y, text, font=MOYENNE_POLICE, fill=None, background=None):
        if id in self.labels:
            raise Exception("Label already in list")
        
        label = tk.Label(self, text=text, font=font, fg=fill, bg=background)
        
        # Positionne le label
        label.place(relx=x, rely=y, anchor='center')
        
        # Ajoute le label à un dictionnaire avec un id unique
        self.labels[id] = {"x": x, "y": y, "text": text, "font": font, "fill": fill, "background": background}
        
        return label

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

        # Lier la molette de la souris pour faire défiler le tableau
        self._bind_mousewheel(None)

    def create_table_from_eleves(self, eleves, criteres):
        """
        Crée un tableau basé sur une liste d'élèves et des critères.
        Affiche le nom, prénom, ID, et les notes pour chaque critère.
        """
        # Définir les titres de colonnes : Prénom, Nom, ID + critères
        self.titre_colonnes = ['Prénom', 'Nom', 'ID']

        # Créer les titres des colonnes
        for j, titre in enumerate(self.titre_colonnes):
            b = tk.Entry(self.frame, disabledbackground="lightgray", disabledforeground="black", font=("Arial", 12), width=15)
            b.insert(0, titre)
            b.configure(state="disabled")
            b.grid(row=0, column=j)

        # Remplir les lignes avec les données des élèves
        for i, eleve in enumerate(eleves):
            # Colonnes fixes : prénom, nom, ID
            entry_prenom = tk.Entry(self.frame, font=("Arial", 12), foreground="black", width=15)
            entry_prenom.insert(0, eleve.prenom)
            entry_prenom.grid(row=i + 1, column=0)

            entry_nom = tk.Entry(self.frame, font=("Arial", 12), foreground="black", width=15)
            entry_nom.insert(0, eleve.nom)
            entry_nom.grid(row=i + 1, column=1)

            entry_id = tk.Entry(self.frame, font=("Arial", 12), foreground="black", width=15)
            entry_id.insert(0, eleve.num_etudiant)
            entry_id.grid(row=i + 1, column=2)

    def _bind_mousewheel(self, event):
        """Lier les événements de la molette de la souris pour le défilement."""
        if event is None or event.widget == self.canvas:
            if self.winfo_toplevel().tk.call('tk', 'windowingsystem') == 'win32':
                self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
            else:
                self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
                self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _unbind_mousewheel(self, event):
        """Délier les événements de la molette de la souris."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel_windows(self, event):
        """Défilement sur Windows."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_mousewheel_linux(self, event):
        """Défilement sur Linux."""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")