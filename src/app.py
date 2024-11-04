import tkinter as tk
from tkinter import ttk
from pages.accueil import *
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EduGroup")
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (PageAccueil,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageAccueil)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

app = App()
app.mainloop()