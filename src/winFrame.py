import tkinter as tk
from src.serialPort import serialPort
import queue
import threading

class winFrame():

    def __init__(self, winObj):
        self.winObj = winObj
        self.winObj.title("Serial Comport Anayser")

        # comport button and its entry
        self.comportLabel = tk.Label(self.winObj, text = "ComPort")
        self.comportLabel.grid(row = 0, column = 0)
        self.comportEntry = tk.Entry(self.winObj)
        self.comportEntry.grid(row=0, column = 1)

        # baudrate button and its entry
        self.baudrateLabel = tk.Label(self.winObj, text = "Baudrate")
        self.baudrateLabel.grid(row=0, column = 2)
        self.baudrateEntry = tk.Entry(self.winObj)
        self.baudrateEntry.grid(row=0, column = 3)

        # connect/disconnect button
        self.connectButton = tk.Button(self.winObj, text = "connect", command = self.connectComport, width = 10)
        self.connectButton.grid(row = 1, column = 3, sticky= tk.E, padx = 10, pady = 10)

        # hex/ascii button
        self.displayButton = tk.Button(self.winObj, text = "ASCII", command = self.displayFormat, width = 10)
        self.displayButton.grid(row = 1, column=0, sticky=tk.W, padx = 10, pady = 10)

        # text widget
        self.textWin = tk.Text(self.winObj)
        self.textWin.grid (row = 2, column = 0, columnspan=4, sticky = tk.NSEW)

        # initial state
        self.comport = ""
        self.baudrate = 0
        self.connection = "disconnect"
        self.displayType = "ASCII"

        self.que = queue.Queue()

    def connectComport(self):
        try:
            self.comport = self.comportEntry.get()
            self.baudrate = self.baudrateEntry.get()

            if self.connection == "disconnect":
                self.connectButton = tk.Button(self.winObj, text="disconnect", command = self.connectComport, width = 10)
                self.connectButton.grid(row=1, column=3, sticky=tk.E, padx=10, pady=10)
                self.connection = "connect"

                self.serialPort = serialPort(port_num = self.comport, baudrate = self.baudrate)
                self.serialPort.open_comport()

                procData = threading.Thread(target = self.processComportData)
                procData.start()

            else:

                self.connectButton = tk.Button(self.winObj, text="connect", command = self.connectComport, width = 10)
                self.connectButton.grid(row=1, column=3, sticky=tk.E, padx=10, pady=10)
                self.connection = "disconnect"

                self.serialPort.close_comport()
                self.textWin.insert(tk.INSERT, self.serialPort.dequeue())

        except Exception as e:
            self.textWin.insert(tk.INSERT, "Unexpected error is received in connectComport() : {}".format(e))


    def processComportData(self):
        try:
            while self.connection == "connect":
                self.serialPort.receiveData(1000)
                while True:
                    msg = self.serialPort.dequeue()
                    if msg != None:
                        if self.displayType == "ASCII":
                            self.textWin.insert(tk.INSERT, msg)
                        else:
                            self.textWin.insert(tk.INSERT, "".join("%02x" % i for i in msg))

                    else:
                        break

        except Exception as e:
            self.textWin.insert(tk.INSERT, "Error in processComportData : {}".format(e))

    def displayFormat(self):
        try:
            if self.displayType == "ASCII":
                self.displayButton = tk.Button(self.winObj, text="HEX", command=self.displayFormat, width=10)
                self.displayButton.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
                self.displayType = "HEX"
            else:
                self.displayButton = tk.Button(self.winObj, text="ASCII", command=self.displayFormat, width=10)
                self.displayButton.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
                self.displayType = "ASCII"

        except Exception as e:
            self.textWin.insert(tk.INSERT, "Error in displayFormat : {}".format(e))

