from tkinter import *
from main_frame import MainFrame

window = Tk()
window.title("Download Youtube")
window.geometry('550x100')
window.resizable(True, True)

mainFrame=MainFrame(window)
mainFrame.pack(expand=True, fill='both')

window.mainloop()