import os
import tkinter as tk
import tkinter.filedialog
def OpenFileDialog(label,is_multi,initDir,filedect,ext):
    fTyp = [(filedect, ext)]
    file_name = []
    iDir = initDir
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