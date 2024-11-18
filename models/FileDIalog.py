import os
import tkinter as tk

def OpenFileDialog(label,is_multi):
    fTyp = [("", "*")]
    file_name = []
    iDir = os.path.abspath(os.path.dirname(__file__))
    if is_multi:
        file_name = tk.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir,title=label)
        check = file_name
    else:
        file_name.append(tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir,title=label))
        check = file_name[0] 

    if len(check) == 0:
        return ""
    else:
        return file_name