import os
import platform
import subprocess
import pandas as pd
from qgis.PyQt.QtWidgets import QFileDialog


def save(df, name, parent_widget=None):
    # Generate default filename

    # Show save file dialog
    if df is None:
        return
    file_path, _ = QFileDialog.getSaveFileName(parent_widget, "Save", name, "CSV Files (*.csv)")
    if not file_path:
        return  # User canceled

    # Save CSV file
    df.to_csv(file_path, index=False)
    print(f"File saved: {file_path}")

    # Open file automatically
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", file_path])
    else:  # Linux and Unix-like systems
        subprocess.call(["xdg-open", file_path])