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