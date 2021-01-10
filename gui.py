import tkinter as tk
import VideoProcess
from tkinter import filedialog, messagebox

VERSION = '0.1'

root = tk.Tk()
try:
    root.tk.call('tk_getOpenFile', '-foobarbaz')
except tk.TclError:
    pass


def main():
    root.title('Tablice v' + VERSION)
    label = tk.Label(root, text="Rozpoznawanie tablic rejestracyjnych wersja " + VERSION)
    label.pack(fill=tk.X)
    # otwieranie
    open_frame = tk.Frame(root)
    open_frame.pack()
    open_label = tk.Label(open_frame, width=21, text='Otwórz plik wejściowy')
    open_label.pack(side=tk.LEFT)
    open_entry = tk.Entry(open_frame, width=25, state='disabled')
    open_entry.pack(side=tk.LEFT)
    open_button = tk.Button(open_frame, text="Otwórz", command=lambda e=open_entry: open_file(e))
    open_button.pack(side=tk.LEFT)
    # zapisywanie
    save_frame = tk.Frame(root)
    save_frame.pack()
    save_label = tk.Label(save_frame, width=21, text='Wskaż katalog wyjściowy')
    save_label.pack(side=tk.LEFT)
    save_entry = tk.Entry(save_frame, width=25, state='disabled')
    save_entry.pack(side=tk.LEFT)
    save_button = tk.Button(save_frame, text="Otwórz", command=lambda e=save_entry: save_file(e))
    save_button.pack(side=tk.LEFT)
    # uruchamianie
    run_frame = tk.Frame(root)
    run_frame.pack()
    run_button = tk.Button(run_frame, width=30, text='Uruchom rozpoznawanie',
                           command=lambda s=save_entry, o=open_entry: run_processing(o, s))
    run_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=False)
    root.mainloop()


def open_file(entry):
    open_filename = filedialog.askopenfilename(initialfile=entry.get())#, filetypes=[("Pliki video", "*.mp4 *.avi")])
    entry.configure(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.insert(tk.END, open_filename)
    entry.configure(state=tk.DISABLED)


def save_file(entry):
    save_filename = filedialog.askdirectory(initialdir=entry.get())
    entry.configure(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.insert(tk.END, save_filename)
    entry.configure(state=tk.DISABLED)


def run_processing(open, save):
    if open.get() != "" and save.get() != "":
        x = VideoProcess.read(open.get(), save.get())
        if x == 1:
            messagebox.showinfo(title="Błąd", message="Podano niepoprawny plik do analizy. Wprowadź plik wideo.")
        else:
            messagebox.showinfo(title="Zakończono", message="Program zakończył pracę")
    else:
        messagebox.showinfo(title="Błąd", message="Uzupełnij dane")

main()
