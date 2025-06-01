import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


def start_nicegui_in_new_process(is_native: bool, port: int):
    mode_arg = "native" if is_native else "browser"
    subprocess.Popen([sys.executable, "main.py", mode_arg, str(port)],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def start_app(port_entry, mode_var, root):
    port = port_entry.get()
    mode = mode_var.get()

    if not port.isdigit():
        messagebox.showerror("Fehler", "Bitte eine gültige Portnummer eingeben.")
        return

    port = int(port)
    is_browser = mode == "browser"

    root.destroy()
    start_nicegui_in_new_process(not is_browser, port)


def start_tk_app():
    root = tk.Tk()
    root.title("Verbindungsoptionen")
    root.geometry("640x480")
    root.resizable(False, False)

    # Port-Label und Entry
    tk.Label(root, text="Port:", font=("Arial", 14)).place(x=180, y=100)
    port_entry = tk.Entry(root, font=("Arial", 14), width=20)
    port_entry.place(x=260, y=100)

    # Port automatisch suchen Button
    def disable_port_entry():
        port_entry.config(state='disabled')
        disable_button.config(state='disabled')

    disable_button = tk.Button(
        root, text="Port automatisch suchen", font=("Arial", 12),
        command=disable_port_entry
    )
    disable_button.place(x=260, y=140)

    # Modus auswählen
    tk.Label(root, text="Modus:", font=("Arial", 14)).place(x=180, y=200)
    mode_var = tk.StringVar(value="browser")
    tk.Radiobutton(root, text="Browser", variable=mode_var, value="browser", font=("Arial", 12)).place(x=260, y=200)
    tk.Radiobutton(root, text="Native", variable=mode_var, value="native", font=("Arial", 12)).place(x=360, y=200)

    # Start-Button
    start_button = tk.Button(
        root, text="Starten", font=("Arial", 14), width=15,
        command=lambda: start_app(port_entry, mode_var, root)
    )
    start_button.place(x=240, y=300)

    root.mainloop()


if __name__ == "__main__":
    start_tk_app()
