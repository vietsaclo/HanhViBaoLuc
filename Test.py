import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
root = tk.Tk()
def change_i():
    if sound_btn.image == icon:
        #start_recording()

        sound_btn.config(image=icon2)
        sound_btn.image = icon2
    else:
        #stop_recording()

        sound_btn.config(image=icon)
        sound_btn.image = icon

icon = PhotoImage(file='FileInput/Icons/ic_tree.png')
icon2 = PhotoImage(file='FileInput/Icons/ic_dir.png')

sound_btn = tk.Button(root, image=icon, width=70,height=60,relief=FLAT ,command=change_i )
sound_btn.image = icon
sound_btn.grid(row=0, column=1)
root.mainloop()