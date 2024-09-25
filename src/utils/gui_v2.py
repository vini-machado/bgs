import tkinter as tk
from tkinter import ttk
from config.database import Mdb
from utils.measurement import get_measurements

from typing import TypedDict

class ReportData(TypedDict):
    report_id: str
    material: str
    manufacturer: str
    temperature: str
    humidity: str

class ExtractorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Extração de dados do BGS")

        # Initialize UI elements
        self.create_widgets()

        # Set window dimensions and center on screen after the widgets are created
        self.window_width = 500
        self.window_height = 400
        self.center_window()

    def center_window(self):
        # Update geometry to make sure the window is rendered
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_x = int((screen_width / 2) - (self.window_width / 2))
        position_y = int((screen_height / 2) - (self.window_height / 2))

        self.root.geometry(f"{self.window_width}x{self.window_height}+{position_x}+{position_y}")

    def create_widgets(self):
        # Instruction label
        label = tk.Label(self.root, text="Selecione um valor:")
        label.pack(pady=10)

        # Create a frame to hold Listbox and Scrollbar
        listbox_frame = tk.Frame(self.root)
        listbox_frame.pack(pady=10)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Listbox with multiple options
        self.listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, width=30, height=10, justify=tk.CENTER, yscrollcommand=scrollbar.set)
        self.populate_listbox()
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Configure scrollbar to work with the listbox
        scrollbar.config(command=self.listbox.yview)

        # Create labels and entry fields for additional data
        self.entries: ReportData = {} 
        self.create_entry("ID do Relatório:", "report_id")
        self.create_entry("Material Avaliado:", "material")
        self.create_entry("Fabricante:", "manufacturer")
        self.create_entry("Temperatura:", "temperature")
        self.create_entry("Umidade:", "humidity")

        # Button to submit the selected value and additional data
        submit_button = tk.Button(self.root, text="Gerar Relatório", command=self.submit_value)
        submit_button.pack(pady=10)

    def create_entry(self, label_text, attr_name):
        tk.Label(self.root, text=label_text).pack(pady=(5, 0))
        entry = tk.Entry(self.root, width=40)
        entry.pack(pady=5)
        self.entries[attr_name] = entry

    def populate_listbox(self):
        for archive in self.get_archives():
            self.listbox.insert(tk.END, archive)

    def get_archives(self):
        with Mdb() as db:
            archives = db.fetch('archives')
        return archives['archive_name'].tolist()

    def submit_value(self):
        selected_indices = self.listbox.curselection()
        selected_archives = [self.listbox.get(i) for i in selected_indices]

        # Get values from the input fields
        report_data = {
            "report_id": self.entries['report_id'].get(),
            "material": self.entries['material'].get(),
            "manufacturer": self.entries['manufacturer'].get(),
            "temperature": self.entries['temperature'].get(),
            "humidity": self.entries['humidity'].get()
        }

        # Call get_measurements or process the collected data as needed
        get_measurements(selected_archives, report_data)


def execute_extractor_window():
    root = tk.Tk()
    app = ExtractorApp(root)
    root.mainloop()
