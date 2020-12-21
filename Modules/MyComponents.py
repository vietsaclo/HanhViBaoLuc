from tkinter import ttk
import tkinter as tk
from Modules import LSTM_Config as cf
from Modules import PublicModules as libs
import datetime
import os

PATH_SAVE_DETECTION = 'FileOutput/Detection'

class TreeActionDetection:
    def __init__(self, containerFather):
        self.containerFather = containerFather
        self.PATH_SAVE_DETECTION = PATH_SAVE_DETECTION
        tree=ttk.Treeview(self.containerFather)
        tree["columns"]=("one")
        tree.column("#0", stretch=tk.NO)
        tree.column("one", stretch=tk.NO)

        tree.heading("#0",text="Name",anchor=tk.W)
        tree.heading("one", text="Date modified",anchor=tk.W)

        # # Level 1
        # folder1=tree.insert("", 1, "", text="Folder 1")
        # tree.insert("", 2, "", text="text_file.txt", values=("23-Jun-17 11:25"))
        # # Level 2
        # tree.insert(folder1, "end", "", text="photo1.png", values=("23-Jun-17 11:28"))
        # tree.insert(folder1, "end", "", text="photo2.png", values=("23-Jun-17 11:29"))
        # tree.insert(folder1, "end", "", text="photo3.png", values=("23-Jun-17 11:30"))

        tree.grid(row=0, column= 0, sticky= 'nsew')
        self.tree = tree
        vsb = ttk.Scrollbar(self.containerFather, orient="vertical", command=tree.yview)
        vsb.grid(row=0, column= 1, sticky= 'nsew')
        self.containerFather.grid_rowconfigure(0, weight=0)
        self.containerFather.grid_columnconfigure(0, weight= 9)
        self.containerFather.grid_columnconfigure(1, weight= 1)

        self.tree.configure(yscrollcommand=vsb.set)

        self.containerFather.grid_rowconfigure(0, weight= 1)
        self.containerFather.grid_columnconfigure(0, weight= 1)

        self.fun_load16Folder()

        # Expand toan bo treee view
        self.open_children(self.tree.focus())

    def fun_load16Folder(self):
        self.arr16Folder = []
        for id in range(0, len(cf.VIDEO_NAMES)):
            folName = cf.VIDEO_NAMES[id]
            fol = self.tree.insert("", id, self.fun_getID_FolderTree(fol= folName), text="Folder {0}".format(folName.upper()))
            self.arr16Folder.append(fol)

    def fun_getID_FolderTree(self, fol:str):
        return 'fol_{0}'.format(fol)

    def fun_saveVideoDetection(self, frames:list, fol:str, bonusFormThread:str = ''):
        folName = self.fun_getID_FolderTree(fol= fol)
        conv, time = self.fun_getCurrentTime()
        fileSave = fol + '_' + conv + '_' + bonusFormThread if bonusFormThread != '' else fol + '_' +  conv

        # AVI extention default
        fileSave += '.avi'

        # make folder if not exists
        self.fun_makeFolder(fol= fol)

        # Save clip to disk
        pathSave = self.PATH_SAVE_DETECTION + '/' + fol
        isSave = libs.fun_saveFramesToVideo(frames= frames, path= pathSave + '/' + fileSave)
        if not isSave:
            libs.fun_print(name= 'Save video: '+ pathSave + '/' + fileSave, value= 'Error: UNKNOW ERROR')

        # Show into GUI
        self.tree.insert(folName, "end", "", text= fileSave, values=(time))

    def open_children(self, parent):
        self.tree.item(parent, open=True)
        for child in self.tree.get_children(parent):
            self.open_children(child)
    
    def fun_getCurrentTime(self, ):
        time = datetime.datetime.now().isoformat()
        res = ''
        for c in time:
            if c == '-' or c == ':' or c == '.':
                res += '_'
            else:
                res += c
        
        return res, time

    def fun_makeFolder(self, fol):
        path = self.PATH_SAVE_DETECTION + '/' + fol
        if not os.path.exists(path= path):
            os.makedirs(name= path)