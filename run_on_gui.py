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
    browse.set(iFilePath)

def conduct_main():
    dir_path = browse.get()
    rmv_bm = remove_all_bookmarks.get()
    if dir_path:
        if dir_path.startswith('{'):
            dir_path = dir_path[1:-1]
        try:
            outdir = anonymization(dir_path, rmv_bm)
            messagebox.showinfo('success', '処理が完了しました。')
            os.startfile(outdir)
        except Exception as e:
            messagebox.showerror('error', f'エラーが発生しました。\n{e.__class__.__name__}: {e}')
    else:
        messagebox.showerror('error', 'パスの指定がありません。')

def drop(event):
    browse.set(event.data)

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
    label1 = ttk.Label(frame1, text='osz file >>', padding=(5, 2))
    label1.pack(side=LEFT)
    # Browse Entry
    browse = StringVar()
    entry1 = ttk.Entry(frame1, textvariable=browse, width=30)
    entry1.pack(side=LEFT)
    # Browse Button
    button1 = ttk.Button(frame1, text='Browse...', command=filedialog_clicked)
    button1.pack(side=LEFT)

    # Frame2
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=1, column=1, sticky=E+W)
    # Run Button
    button2_1 = ttk.Button(frame2, text='Run', width=20, command=conduct_main)
    button2_1.pack(fill = 'x', padx=20, side='right')
    # Check Box
    remove_all_bookmarks = BooleanVar()
    button2_2 = ttk.Checkbutton(frame2, text='Remove all bookmarks', variable=remove_all_bookmarks)
    button2_2.pack(fill = 'x', padx=20, side='right')

    root.mainloop()