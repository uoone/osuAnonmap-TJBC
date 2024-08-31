import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinterdnd2 import *

from main import anonymization

def filedialog_clicked():
    fTyp = [('', '*')]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    entry.set(iFilePath)

def conduct_main():
    dirPath = entry.get()
    if dirPath:
        if dirPath.startswith('{'):
            dirPath = dirPath[1:-1]
        outdir = anonymization(dirPath)
        messagebox.showinfo('success', '処理が完了しました。')
        os.startfile(outdir)
    else:
        messagebox.showerror('error', 'パスの指定がありません。')

def drop(event):
    entry.set(event.data)

if __name__ == '__main__':
    root = Tk()
    root.title('osuTaikoAnonmap gui edition')
    root.resizable(False, False)
    root.iconbitmap(default='./resource/taiko.ico')
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)

    # Frame1
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=0, column=1, sticky=E+W)
    # Browse
    IFileLabel = ttk.Label(frame1, text='osz file >>', padding=(5, 2))
    IFileLabel.pack(side=LEFT)
    # Browse Entry
    entry = StringVar()
    IFileEntry = ttk.Entry(frame1, textvariable=entry, width=30)
    IFileEntry.pack(side=LEFT)
    # Browse Button
    IFileButton = ttk.Button(frame1, text='Browse...', command=filedialog_clicked)
    IFileButton.pack(side=LEFT)

    # Frame2
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=1, column=1, sticky=E+W)
    # Run Button
    button1 = ttk.Button(frame2, text='Run', width=20, command=conduct_main)
    button1.pack(fill = 'x', padx=20, side='right')

    root.mainloop()