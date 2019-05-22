import serial
import tkinter as tk

from src.winFrame import winFrame

if __name__ == "__main__":
    rootWin = tk.Tk()
    winMain = winFrame(rootWin)
    rootWin.mainloop()
