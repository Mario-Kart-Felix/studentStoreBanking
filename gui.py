#!/usr/bin/python3
from tkinter import *
from nfcScript import *
from database import database

class store:

    def __init__(self, master):
        self.root = master
        self.frame = Frame(self.root)
        self.textBox = Text(self.frame)
        self.textBox.insert(INSERT, "Welcome to the store!")
        self.clearText = Button(self.frame)
        self.scan = Button(self.frame)
        self.addBalButton = Button(self.frame)
        self.subBalButton = Button(self.frame)
        self.addAccButton = Button(self.frame)
        self.defaultButtons()
        self.defaultLayout()
        self.createKeyPad()

        self.db = database()
        self.currentUser = None

    def defaultButtons(self):
        self.clearText.config(text="Clear", command=lambda: self.textBox.delete(1.0, END))
        self.scan.config(text="Scan Card", command=self.scanCard)
        self.addBalButton.config(text="Add Balance", command=self.addBalance)
        self.subBalButton.config(text="Subtract Balance", command=self.subBalance)
        self.addAccButton.config(text="Add Account", command=self.addAccountStage)


    def defaultLayout(self):
        self.addBalButton.grid_forget()
        self.subBalButton.grid_forget()
        self.frame.grid(row=0, column=0)
        self.textBox.grid(row=0, column=4, rowspan=4, columnspan=3)
        self.scan.grid(row=4, column=4)
        self.clearText.grid(row=4, column=5)
        self.addAccButton.grid(row=4, column=6)

    # On press of scan button switch layout.
    def scanLayout(self):
        self.scan.grid_forget()
        self.addAccButton.grid_forget()
        self.subBalButton.grid(row=4, column=6)
        self.addBalButton.grid(row=4, column=4)


    def createKeyPad(self):
        keypad = [7,8,9,4,5,6,1,2,3,0,".","Enter\nReturn"]
        r = 1
        c = 0
        for i in keypad:
            valuePress = lambda button=i: store.printMessage(self, button)
            Button(self.frame, text=i, command=valuePress, height=5, width=3).grid(row=r,column=c)
            c+=1
            if c >= 3:
                c = 0
                r+=1

    def retrieve_input(self, lines=1):
        # pulls just the last line for cleanup reasons. May modify function to take multiple lines
        return self.textBox.get("1.0", 'end-1c').splitlines()[-lines:]

    def scanCard(self):
        self.scanLayout()
        self.printMessage("\nPlace card on reader.")
        x = decode()
        if not x:  # if the reader throws an error.
            self.printMessage("\nMake sure the reader is plugged in and turned on.")
        else:
            self.currentUser = x
            name = self.db.getStudentName(x)
            if bool(name[len(name)-1]):  # if the call returns true, then do the following.
                balance = self.db.getBalance(x)
                self.printMessage("\nID: " + x + "\nStudent Name: " + name[0] + "\nBalance: $" + str(round(balance[0],2)))
                self.printMessage("\nType the balance you would like to add or subtract: ")
                self.clearText.config(command=self.abort)
            else:
                self.printMessage("\nNo account found!")
                self.defaultLayout()



    def printMessage(self, text):
        if text != "Enter\nReturn":
            self.textBox.insert(END, str(text))
        else:
            self.textBox.insert(END, "\n")
        self.textBox.update()

    def abort(self):
        self.defaultLayout()
        self.defaultButtons()

    def addBalance(self, negative=False):
        inputlines = self.retrieve_input(1)
        difference = float(inputlines[0][inputlines[0].index(":")+2:])
        if negative:
            difference = -difference
        proc = self.db.changeBalance(self.currentUser, difference)
        if bool(proc[len(proc)-1]):  # if the call returns true, then do the following
            self.printMessage("\nBalance was changed.")
            bal = round(self.db.getBalance(self.currentUser)[0],2)
            self.printMessage("\nNew balance is: " + str(bal))
        else:
            self.printMessage("\nBalance would be below zero")
        self.abort()

    def subBalance(self):
        self.addBalance(True)

    def addAccountStage(self):
        self.printMessage("\nPlace card on reader.")
        x = decode()
        if not x:  # if the reader throws an error.
            self.printMessage("\nMake sure the reader is plugged in and turned on.")
        else:
            self.currentUser = x
            self.clearText.config(command=self.abort)
            name = self.db.getStudentName(x)
            if not bool(name[len(name)-1]):  # if the call returns true, then do the following.
                self.printMessage("\nOn each line type in the required information then press the Add Account Button. ")
                self.printMessage("\nName: ")
                self.printMessage("\nBalance: ")
                self.addAccButton.config(command=self.addAccountCommit)

            else:
                self.printMessage("\nAccount already exists: it belongs to " + name[0])

    def addAccountCommit(self):
        inputlines = self.retrieve_input(2)
        name = inputlines[0][inputlines[0].index(":")+2:]
        balance = float(inputlines[1][inputlines[1].index(":")+2:])
        proc = self.db.addAccount(self.currentUser,name,balance)
        if bool(proc[len(proc)-1]):  # if the call returns true, then do the following
            self.printMessage("\nAccount Created!")
        else:
            self.printMessage("Something went wrong...")
        self.defaultButtons()



storeWindow = Tk()
store(storeWindow)
storeWindow.mainloop()
