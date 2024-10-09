import tkinter as tk
import traceback
from dataclasses import dataclass
from tkinter import messagebox
from typing import Optional

from config.database import Mdb
from utils.report import generate_report


@dataclass
class Field:
    identifier: str
    label: str
    input_value: Optional[tk.Entry] = None

    def get_input(self):
        if isinstance(self.input_value, tk.Entry):
            return {self.identifier: self.input_value.get()}
        return {self.identifier: ""}


class FormData:
    def __init__(self, root: tk.Frame, fields: list[Field]) -> None:
        self.root = root
        self.fields = fields

        self.create_input_field()

    def create_input_field(self):
        for index, field in enumerate(self.fields):
            tk.Label(self.root, text=field.label).grid(
                row=index, column=0, padx=10, pady=5, sticky="e"
            )
            entry = tk.Entry(self.root, width=40)
            entry.grid(row=index, column=1, padx=10, pady=5)
            field.input_value = entry

    def extract_inputs(self):
        data = {}
        for field in self.fields:
            data = data | field.get_input()
        return data


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

        # Configure grid for dynamic resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def center_window(self):
        # Update geometry to make sure the window is rendered
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = int((screen_width / 2) - (self.window_width / 2))
        position_y = int((screen_height / 2) - (self.window_height / 2))
        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{position_x}+{position_y}"
        )

    def create_widgets(self):
        # Create main frame for better organization
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create left frame for listbox
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Instruction label
        label = tk.Label(listbox_frame, text="Selecione um valor:")
        label.pack(pady=10)

        # Create a Listbox with multiple options
        self.listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            width=30,
            height=10,
            justify=tk.CENTER,
        )
        self.populate_listbox()
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Add scrollbar for listbox
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Create right frame for form fields
        form_frame = tk.Frame(main_frame)
        form_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create labels and entry fields for additional data
        self.formdata = FormData(
            root=form_frame,
            fields=[
                Field(identifier="report_id", label="ID do Relatório:"),
                Field(identifier="material", label="Material Avaliado:"),
                Field(identifier="manufacturer", label="Fabricante:"),
                Field(identifier="temperature", label="Temperatura:"),
                Field(identifier="humidity", label="Umidade:"),
            ],
        )

        # Button to submit the selected value and additional data
        submit_button = tk.Button(
            form_frame, text="Gerar Relatório", command=self.submit_value
        )
        submit_button.grid(
            row=len(self.formdata.fields) + 1, column=0, columnspan=2, pady=10
        )

    def populate_listbox(self):
        with Mdb() as db:
            archives = db.fetch("archives")
        options = archives["archive_name"].tolist()

        for option in options:
            self.listbox.insert(tk.END, option)

    def submit_value(self):
        selected_indices = self.listbox.curselection()
        selected_archives = [self.listbox.get(i) for i in selected_indices]

        # Get values from the input fields
        try:
            report_data = self.formdata.extract_inputs()
            generate_report(report_data, selected_archives)

            # messagebox.showinfo("Success", "Report generated successfully!")
        except Exception as e:
            messagebox.showerror(type(e).__name__, traceback.format_exc())
