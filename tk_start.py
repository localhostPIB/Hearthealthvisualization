import subprocess
import logging
import sys
import tkinter as tk
from tkinter import messagebox


def start_nicegui_in_new_process(is_native: bool, port: int, automatic_port: bool,root):
    try:
        mode_arg = "native" if is_native else "browser"
        port_arg = str(port) if automatic_port else str(port)
        process = subprocess.Popen([sys.executable, "main.py", mode_arg, str(port), str(port_arg)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        _, stderr_output = process.communicate(timeout=2)

        if stderr_output:
            raise RuntimeError(stderr_output.decode("utf-8"))
        root.destroy()
    except subprocess.TimeoutExpired:
        pass

    except RuntimeError as e:
        logging.exception(f"Fehler beim Starten von main.py: {type(e).__name__}")
        messagebox.showerror("Fehler", f"Fehler beim Starten: {type(e).__name__}")


def start_app(port_entry, mode_var, disable_button, root):
    port = port_entry.get()
    mode = mode_var.get()
    port_locked = getattr(disable_button, "was_pressed", False)

    if not port_locked and not port.isdigit() and 1024 <= port <= 49151:
        messagebox.showerror("Fehler", "Bitte eine gültige Portnummer eingeben.")
        return

    is_browser = mode == "browser"

    try:
        if not port_locked:
            port = int(port)
            start_nicegui_in_new_process(not is_browser, port, not port_locked,root)
        else:
            start_nicegui_in_new_process(not is_browser, 5000, not port_locked,root)
    except Exception as e:
        logging.exception("Fehler beim Starten von main.py")
        error_type = type(e).__name__
        messagebox.showerror("Fehler", f"{error_type}: {e}")


def start_tk_app():
    root = tk.Tk()
    root.title("🩺 Verbindungsoptionen")
    root.geometry("550x450")
    root.resizable(False, False)

    tk.Label(root, text="Port:", font=("Arial", 14)).place(relx=0.3, rely=0.25, anchor="e")

    port_entry = tk.Entry(root, font=("Arial", 14), width=20,state='disabled')
    port_entry.place(relx=0.3, rely=0.25, anchor="w")

    def toggle_port_entry():
        if port_entry["state"] == "normal":
            port_entry.config(state="disabled")
            disable_button.was_pressed = True
            disable_button.config(text="Port manuell eingeben")
        else:
            port_entry.config(state="normal")
            disable_button.was_pressed = False
            disable_button.config(text="Port automatisch suchen")

    disable_button = tk.Button(root, text="Port manuell eingeben", font=("Arial", 12), command=toggle_port_entry)

    disable_button.place(relx=0.5, rely=0.35, anchor="center")
    disable_button.was_pressed = True

    tk.Label(root, text="Modus:", font=("Arial", 14)).place(relx=0.5, rely=0.50, anchor="e")

    mode_var = tk.StringVar(value="browser")
    (tk.Radiobutton(root, text="Im Browser starten", variable=mode_var, value="browser", font=("Arial", 12))
     .place(relx=0.3, rely=0.55, anchor="w"))
    (tk.Radiobutton(root, text="Im eigenen Fenster starten (native)", variable=mode_var, value="native", font=("Arial", 12))
     .place(relx=0.3, rely=0.60, anchor="w"))

    start_button = tk.Button(
        root, text="Starten", font=("Arial", 14), width=15,
        command=lambda: start_app(port_entry, mode_var, disable_button, root)
    )
    start_button.place(relx=0.5, rely=0.75, anchor="center")

    root.mainloop()


if __name__ == "__main__":
    start_tk_app()
