import tkinter as tk
from tkinter.ttk import Treeview, Scrollbar

from gui.utils import validate_positive
from service import save_heart_service, get_all_heart_service, make_line_plot_service, save_plot_to_pdf
from tkinter.filedialog import asksaveasfilename


class MainFrame:

    def __init__(self, root):
        icon_path = "ressource/img/heart-1151624_1280.ico"
        root.iconbitmap(icon_path)
        validation = root.register(validate_positive)

        root.title('Gesundheit')
        self.systolischer_value = tk.IntVar()
        self.diastolischer_value = tk.IntVar()
        self.puls_value = tk.IntVar()

        label_systolisch = tk.Label(text="Systolischer Wert: ")
        label_diastolisch = tk.Label(text="Diastolisch Wert: ")
        label_puls = tk.Label(text="Puls: ")

        self.inputfield_systolisch = tk.Entry(textvariable=self.systolischer_value)
        self.inputfield_diastolisch = tk.Entry(textvariable=self.diastolischer_value)
        self.inputfield_puls = tk.Entry(textvariable=self.puls_value)

        self.inputfield_systolisch.place(x=200, y=10)
        self.inputfield_diastolisch.place(x=200, y=35)
        self.inputfield_puls.place(x=200, y=60)
        label_systolisch.place(x=10, y=10)
        label_diastolisch.place(x=10, y=30)
        label_puls.place(x=10, y=50)
        plotbutton = tk.Button(text="Grafische Auswertung (Browser)",
                               command=lambda: self.get_plot(get_all_heart_service(), False))
        plotbutton.place(x=15, y=350)
        savepdfbutton = tk.Button(root, text="Grafische Auswertung als PDF", command=lambda: self.save_file())
        savepdfbutton.place(x=800, y=350)
        savebutton = tk.Button(text="Werte speichern", command=lambda: self.save_heart_value(tree)
                                                                       and self.switch_buttons(plotbutton))
        savebutton.place(x=15, y=70)
        self.switch_buttons(plotbutton)
        self.switch_buttons(savepdfbutton)

        columns = ('systolic_BP', 'diastolic_BP', 'puls_Frequency', 'date', 'time')
        tree = Treeview(root, columns=columns, show='headings')

        tree.heading('systolic_BP', text='Systolisch')
        tree.heading('diastolic_BP', text='Diastolisch')
        tree.heading('puls_Frequency', text='Puls')
        tree.heading('date', text='Datum')
        tree.heading('time', text='Uhrzeit')

        self.build_tree(tree)

        tree.place(x=20, y=100)

        scrollbar = Scrollbar(orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.place(x=1025, y=100, height=230)

        tree.update()

    def save_file(self):
        pdf_file = asksaveasfilename(initialfile='Health.pdf',
                                     defaultextension=".pdf", filetypes=[("Text Documents", "*.pdf")])
        plot = self.get_plot(self.get_all_heart_value(), True)

        if not pdf_file is '':
            save_plot_to_pdf(plot, pdf_file)

    def save_heart_value(self, tree):
        save_heart_service(int(self.inputfield_systolisch.get()),
                           int(self.inputfield_diastolisch.get()),
                           int(self.inputfield_puls.get()))

        self.build_tree(tree)

    def switch_buttons(self, button):
        if not get_all_heart_service():
            button["state"] = "disabled"
        else:
            button["state"] = "normal"

    def get_all_heart_value(self):
        return get_all_heart_service()

    def build_tree(self, tree):
        for i in tree.get_children():
            tree.delete(i)

        for heart_value in self.get_all_heart_value():
            tree.insert("", tk.END, values=heart_value)

    def get_plot(self, data, save: bool):
        return make_line_plot_service(data, save)
