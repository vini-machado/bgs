import tkinter as tk
from tkinter import ttk
from config.database import Mdb
from utils.measurement import get_measurements

def get_archives():
    with Mdb() as db:
        archives = db.fetch('archives')
    return archives['archive_name'].tolist()     

def execute_extractor_window():
    def submit_value(listbox: tk.Listbox):
        selected_indices = listbox.curselection()
        selected_archives = [listbox.get(i) for i in selected_indices]
        
        # Get values from the input fields
        report_data = {
            "report_id": report_id_entry.get(),
            "material": material_entry.get(),
            "manufacturer": manufacturer_entry.get(),
            "temperature": temperature_entry.get(),
            "humidity": humidity_entry.get()
        }

        # Call get_measurements or process the collected data as needed
        get_measurements(selected_archives, report_data)

    # Create the main window
    root = tk.Tk()
    root.title("Extração de dados do BGS")

    # Centralize the window on the screen
    window_width = 500
    window_height = 400
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    position_x = int((screen_width / 2) - (window_width / 2))
    position_y = int((screen_height / 2) - (window_height / 2))

    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Instruction label
    label = tk.Label(root, text="Selecione um valor:")
    label.pack(pady=10)

    # Create a Listbox with multiple options
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=20, height=10, justify=tk.CENTER)
    for archive in get_archives():
        listbox.insert(tk.END, archive)
    listbox.pack(pady=10)

    # Create labels and entry fields for additional data
    tk.Label(root, text="ID do Relatório:").pack(pady=(5, 0))
    report_id_entry = tk.Entry(root, width=40)
    report_id_entry.pack(pady=5)

    tk.Label(root, text="Material Avaliado:").pack(pady=(5, 0))
    material_entry = tk.Entry(root, width=40)
    material_entry.pack(pady=5)

    tk.Label(root, text="Fabricante:").pack(pady=(5, 0))
    manufacturer_entry = tk.Entry(root, width=40)
    manufacturer_entry.pack(pady=5)

    tk.Label(root, text="Temperatura:").pack(pady=(5, 0))
    temperature_entry = tk.Entry(root, width=40)
    temperature_entry.pack(pady=5)

    tk.Label(root, text="Umidade:").pack(pady=(5, 0))
    humidity_entry = tk.Entry(root, width=40)
    humidity_entry.pack(pady=5)

    # Button to submit the selected value and additional data
    submit_button = tk.Button(root, text="Gerar Relatório", command=lambda: submit_value(listbox))
    submit_button.pack(pady=10)

    # Execute the window
    root.mainloop()
