import os
import platform


def open_excel_file(file_path: str):
    if os.path.exists(file_path):
        # Determine the operating system and open the file with the default application
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{file_path}'")
        else:  # Assume Linux or other systems
            os.system(f"xdg-open '{file_path}'")
    else:
        print(f"File not found: {file_path}")
