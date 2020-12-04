import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

VERSION = '0.1'

root = tk.Tk()
try:
    root.tk.call('tk_getOpenFile', '-foobarbaz')
except tk.TclError:
    pass
root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')


def main():
    root.title('Tablice v' + VERSION)
    label = tk.Label(root, text="Rozpoznawanie tablic rejestracyjnych wersja " + VERSION)
    label.pack(fill=tk.X)
    # otwieranie
    open_frame = tk.Frame(root)
    open_frame.pack()
    open_label = tk.Label(open_frame, width=21, text='Otworz plik wejsciowy')
    open_label.pack(side=tk.LEFT)
    open_entry = tk.Entry(open_frame, width=25)
    open_entry.pack(side=tk.LEFT)
    open_button = tk.Button(open_frame, text="Otworz", command=lambda e=open_entry: open_file(e))
    open_button.pack(side=tk.LEFT)
    # zapisywanie
    save_frame = tk.Frame(root)
    save_frame.pack()
    save_label = tk.Label(save_frame, width=21, text='Wskaz katalog wyjsciowy')
    save_label.pack(side=tk.LEFT)
    save_entry = tk.Entry(save_frame, width=25)
    save_entry.pack(side=tk.LEFT)
    save_button = tk.Button(save_frame, text="Zapisz", command=lambda e=save_entry: save_file(e))
    save_button.pack(side=tk.LEFT)
    # uruchamianie
    run_frame = tk.Frame(root)
    run_frame.pack()
    run_button = tk.Button(run_frame, width=30, text='Uruchom',
                           command=lambda s=save_entry, o=open_entry: run_processing(o, s))
    run_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=False)
    root.mainloop()


def open_file(entry):
    open_filename = filedialog.askopenfilename(initialfile=entry.get(), filetypes=[("MP4", "*.mp4")])
    entry.delete(0, tk.END)
    entry.insert(tk.END, open_filename)


def save_file(entry):
    save_filename = filedialog.askdirectory(initialdir=entry.get())
    entry.delete(0, tk.END)
    entry.insert(tk.END, save_filename)


def run_processing(open, save):
    # tutaj odpalanie
    print(open.get(), save.get())


main()