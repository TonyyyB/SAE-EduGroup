import tkinter as tk
from tkinter import ttk

# Font constants for styling
GRANDE_POLICE = ("Helvetica", 16, "bold")
PETITE_POLICE = ("Helvetica", 12)

class PageDefGroupe(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Total number of students (for remaining calculation)
        self.total_students = 40  # Placeholder for the total number of students

        # Title Label
        title_label = ttk.Label(self, text="Définition des paramètres de groupes", font=GRANDE_POLICE, foreground="white", background="#2C3E50")
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Background color for entire frame
        self.configure(bg="#2C3E50")

        # "Nombre de groupes en sortie" label and entry
        group_count_label = ttk.Label(self, text="Nombre de groupes en sortie:", font=PETITE_POLICE, background="#2C3E50", foreground="white")
        group_count_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.group_count_entry = tk.Entry(self, width=5)
        self.group_count_entry.insert(0, "5")  # Default value
        self.group_count_entry.grid(row=1, column=1, padx=10, pady=10)
        self.group_count_entry.bind("<KeyRelease>", self.update_groups)  # Update group entries dynamically

        # Frame for vertical slider and group entries
        self.slider_frame = tk.Frame(self, bg="#2C3E50")
        self.slider_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0), padx=10, sticky="nsew")

        # Canvas for scrolling content
        self.canvas = tk.Canvas(self.slider_frame, width=400, height=200, bg="#2C3E50", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.slider_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame inside canvas to hold group entries
        self.groups_frame = tk.Frame(self.canvas, bg="#2C3E50")
        self.canvas.create_window((0, 0), window=self.groups_frame, anchor="nw")

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # "Nombre d'élèves restant à placer" label and entry
        remaining_label = ttk.Label(self, text="Nombre d'élèves restant à placer:", font=PETITE_POLICE, background="#2C3E50", foreground="white")
        remaining_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.remaining_entry = tk.Entry(self, width=5, state="disabled")  # Display remaining students
        self.remaining_entry.insert(0, "0")
        self.remaining_entry.grid(row=3, column=1, padx=10, pady=10)

        # "Suivant" button
        self.next_button = ttk.Button(self, text="Suivant", command=lambda: controller.show_frame(PageAccueil))
        self.next_button.grid(row=4, column=0, columnspan=2, pady=(20, 10))
        self.next_button["state"] = "disabled"  # Initially disabled until all students are placed

        # Back button
        back_button = ttk.Button(self, text="Retour", command=lambda: controller.show_frame(PageAccueil))
        back_button.grid(row=0, column=2, padx=(0, 20))

        # Configure grid layout for responsiveness
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.update_groups()  # Initial call to set up group entries

    def update_groups(self, event=None):
        # Get number of groups from entry
        try:
            num_groups = int(self.group_count_entry.get())
            if num_groups < 1:
                return  # Ignore invalid values
        except ValueError:
            return  # Ignore invalid entries

        # Clear previous entries in groups_frame
        for widget in self.groups_frame.winfo_children():
            widget.destroy()

        # Add entries for each group
        self.group_entries = []
        for i in range(num_groups):
            group_label = ttk.Label(self.groups_frame, text=f"Groupe {i + 1}", font=PETITE_POLICE, background="#2C3E50", foreground="white")
            group_label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

            group_entry = tk.Entry(self.groups_frame, width=5)
            group_entry.insert(0, "0")  # Default value for each group
            group_entry.grid(row=i, column=1, padx=10, pady=5)
            group_entry.bind("<KeyRelease>", self.update_remaining_students)  # Recalculate remaining students on change
            self.group_entries.append(group_entry)

        # Update scroll region for the canvas to fit new content
        self.groups_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.update_remaining_students()  # Initial calculation of remaining students

    def update_remaining_students(self, event=None):
        # Calculate the remaining students based on current group entries
        total_assigned = 0
        for entry in self.group_entries:
            try:
                count = int(entry.get())
                if count < 0:
                    count = 0  # Ignore negative values
                total_assigned += count
            except ValueError:
                pass  # Ignore invalid entries

        remaining = self.total_students - total_assigned
        self.remaining_entry.configure(state="normal")
        self.remaining_entry.delete(0, tk.END)
        self.remaining_entry.insert(0, str(remaining))
        self.remaining_entry.configure(state="disabled")

        # Enable or disable "Suivant" button based on remaining students
        if remaining == 0:
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"
