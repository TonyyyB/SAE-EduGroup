import tkinter as tk

class TableRow(tk.Frame):
    def __init__(self, parent, data, table, dad=False):
        super().__init__(parent)
        self.table = table  # Référence à la table parente
        self.data = data    # Données de la ligne
        self.items = []

        # Création des colonnes pour la ligne
        for i, item in enumerate(data):
            if isinstance(item, (int, float, str)):
                lbl = tk.Label(self, text=item, bg="white", font=("Arial", 12))
            else:
                lbl.master = item
                lbl = item
            lbl.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            self.items.append(lbl)
            if dad:
                # Bind des événements sur chaque cellule
                lbl.bind("<ButtonPress-1>", self.start_drag)
                lbl.bind("<B1-Motion>", self.do_drag)
                lbl.bind("<ButtonRelease-1>", self.stop_drag)
        if dad:
            self.drag_data = {"x": 0, "y": 0, "offset_x": 0, "offset_y": 0}
        table.update_idletasks()

    def start_drag(self, event):
        """Commence le drag de la ligne."""
        self.drag_data["x"] = event.x_root
        self.drag_data["y"] = event.y_root
        self.drag_data["offset_x"] = event.x
        self.drag_data["offset_y"] = event.y
        self.lift()
        self.configure(bg="lightyellow")  # Effet visuel

        # Déplacer temporairement dans le parent commun
        self.place(in_=self.table.controller, x=event.x_root - self.table.controller.winfo_rootx() - self.drag_data["offset_x"],
                   y=event.y_root - self.table.controller.winfo_rooty() - self.drag_data["offset_y"])

    def do_drag(self, event):
        """Déplace la ligne pendant le drag."""
        x = event.x_root - self.table.controller.winfo_rootx() - self.drag_data["offset_x"]
        y = event.y_root - self.table.controller.winfo_rooty() - self.drag_data["offset_y"]
        self.place(x=x, y=y)

    def stop_drag(self, event):
        """Gère le drop sur la table cible."""
        self.configure(bg="white")
        x_root, y_root = self.winfo_pointerx(), self.winfo_pointery()

        # Vérifie la table cible
        target_table = None
        for table in self.table.controller.tables:
            if table.is_pointer_inside(x_root, y_root):
                target_table = table
                break

        # Si drop sur une table cible, déplace la ligne
        if target_table:
            self.place_forget()
            self.table.remove_row(self)  # Retire la ligne de la table actuelle
            target_table.add_row(self.data)  # Ajoute la ligne à la nouvelle table
            self.destroy()
        else:
            # Si drop hors table, replacer dans la table d'origine
            self.place_forget()
            self.table.add_row(self.data)
            self.destroy()


class Table(tk.Frame):
    def __init__(self, parent, headers, controller=None, enable_scroll_x=False, enable_scroll_y=False):
        super().__init__(parent)
        self.controller = controller
        self.headers = headers
        self.rows = []

        # Enregistre cette table
        if self.controller is not None: self.controller.tables.append(self)

        # Canvas pour permettre les déplacements
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        if enable_scroll_x:
            self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.scrollbar_x.grid(row=1, column=0, sticky="ew")
            self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        if enable_scroll_y:
            self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.scrollbar_y.grid(row=0, column=1, sticky="ns")
            self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Création des en-têtes
        header_frame = tk.Frame(self.canvas)
        for i, header in enumerate(headers):
            lbl = tk.Label(header_frame, text=header, bg="lightgray", font=("Arial", 12))
            lbl.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        self.canvas.create_window((0, 0), window=header_frame, anchor="nw")
        header_frame.grid(row=0, column=0, sticky="nsew")
    
    def adjust_column_widths(self):
        """Ajuste la largeur des colonnes selon le plus large élément de chaque colonne."""
        if not self.rows:
            return
        
        num_columns = len(self.headers)
        column_widths = [0] * num_columns  # Stocke la largeur max de chaque colonne

        # Parcours des lignes et mise à jour des largeurs
        for row in self.rows:
            for i, widget in enumerate(row.items):
                widget.update_idletasks()  # Assure que les dimensions sont mises à jour
                width = widget.winfo_reqwidth()
                column_widths[i] = max(column_widths[i], width)

        # Appliquer la largeur maximale trouvée à chaque colonne
        for row in self.rows:
            for i, widget in enumerate(row.items):
                widget.config(width=column_widths[i] // 10)  # Ajuste `width` (tkinter utilise unités de caractères)
        
        # Mise à jour de l'affichage
        self.update_idletasks()

    def add_row(self, data):
        """Ajoute une nouvelle ligne dans la table."""
        row = TableRow(self.controller, data, self, dad=self.controller is not None)
        row.grid(in_=self.canvas, row=len(self.rows) + 1, column=0, columnspan=len(self.headers), sticky="nsew", pady=1)
        self.rows.append(row)
        
        # Ajustement automatique des colonnes
        self.adjust_column_widths()


    def remove_row(self, row):
        """Retire une ligne de la table."""
        if row in self.rows:
            self.rows.remove(row)
            row.destroy()

    def is_pointer_inside(self, x, y):
        """Vérifie si le pointeur est à l'intérieur de la table."""
        x1, y1 = self.winfo_rootx(), self.winfo_rooty()
        x2, y2 = x1 + self.winfo_width(), y1 + self.winfo_height()
        return x1 <= x <= x2 and y1 <= y <= y2

class DragAndDropController():
    def __init__(self):
        self.tables = []

# ---- APP PRINCIPALE ----

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Table avec Drag and Drop")
        self.geometry("800x400")
        self.tables = []  # Liste de toutes les tables

        # Créer deux tables
        table1 = Table(self, self, ["Prénom", "Nom", "ID"])
        table1.grid(row=0, column=0, padx=20, pady=20)

        table2 = Table(self, self, ["Prénom", "Nom", "ID"])
        table2.grid(row=0, column=1, padx=20, pady=20)

        # Remplir la première table
        table1.add_row(["Alice", "Dupont", "001"])
        table1.add_row(["Bob", "Martin", "002"])
        table1.add_row(["Clara", "Durand", "003"])


if __name__ == "__main__":
    app = App()
    app.mainloop()