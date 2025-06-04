import subprocess
import logging
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from exception import NiceGUINotStartedException


def start_nicegui_in_new_process(is_native: bool, port: int, automatic_port: bool,root):
    """
    Starts the Nicegui app, a command is passed to start, and all errors are output.
    
    :param is_native: The app (Nicegui) can be started as a separate window or in the browser
    :param port: Which port was specified
    :param automatic_port: Should nicegui take care of a free port?
    :param root: Handling the thinter app
    """ 
    try:
        mode_arg = "native" if is_native else "browser"
        port_arg = str(port) if automatic_port else str(port)
        process = subprocess.Popen([sys.executable, "main.py", mode_arg, str(port), str(port_arg)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        root.nicegui_process = process

        _, stderr_output = process.communicate(timeout=2)

        if stderr_output:
            raise NiceGUINotStartedException(stderr_output.decode("utf-8"))
        root.destroy()
    except subprocess.TimeoutExpired:
        pass

    except NiceGUINotStartedException as e:
        logging.exception(f"Fehler beim Starten von main.py: {type(e).__name__}")
        messagebox.showerror("Fehler", f"Fehler beim Starten: {type(e).__name__}")


def start_app(port_entry, mode_var, disable_button, root):
    """
    Checks and validates the user's entries
    
    :param port_entry: The entry for the port.
    :param mode_var: Browser or Native mode.
    """ 
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

def stop_app(root):
    """
    Closes the Nicegui app so that the system also releases the port. The tkinter program will also be closed.
    
    :param root: The added attributes are used to close the Nicegui process.
    """ 
    if hasattr(root, "nicegui_process"):
        root.nicegui_process.terminate()
        root.nicegui_process.wait(timeout=1)


def start_tk_app():
    """
    The gui is assembled here.
    """ 
    root = tk.Tk()
    root.title("🩺 Verbindungsoptionen")
    root.geometry("550x450")
    root.resizable(False, False)

    image = Image.open("resources/static/img/blood_pressure.jpg.jpg")
    image = image.resize((800, 600))
    photo = ImageTk.PhotoImage(image)

    background_label = tk.Label(root, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(root, text="Port:", font=("Arial", 14)).place(relx=0.3, rely=0.25, anchor="e")

    port_entry = tk.Entry(root, font=("Arial", 14), width=20, state='disabled')
    port_entry.place(relx=0.32, rely=0.25, anchor="w")

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
    exit_button = tk.Button(root, text="Beende Gesundheitsmonitor", font=("Arial", 12), command=lambda: (stop_app(root), root.destroy()))

    exit_button.place(relx=0.5, rely=0.9, anchor="center")

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
    """
    The tkinter app is intended to create a kind of utility program to select the port for the Nicegui app to start
    the native windows and close it again to release the port.
    """ 
    start_tk_app()
