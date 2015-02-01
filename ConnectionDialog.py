__author__ = 'Derar'
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import Relation
import xmlReader
import FunctionalDependency
from Relation import Relation
from DBSchema import Dbschema

class ConnectionDialog():
    def __init__(self,parent):

        window = self.top = Toplevel(parent)
        window.transient(parent)
        window.grab_set()
        window.title("Database Connection")
        window.geometry("275x175+30+30")

        #1st row *** Username***
        self.labelUsername = Label(window, text="Username (*):")
        self.labelUsername.grid(row=0, column=0, padx=10, pady=2, sticky=NW)


        self.entryUsername = Entry(window)
        self.entryUsername["width"] = 20
        self.entryUsername.focus_set()
        self.entryUsername.grid(row=0, column=1, padx=10, sticky=E)
        self.entryUsername.insert(0, "postgres")
        #2nd row *****password*****
        self.labelPassword = Label(window, text="Password:")
        self.labelPassword.grid(row=1, column=0, padx=10, pady=2, sticky=W)

        self.entryPassword = Entry(window, show="*")
        self.entryPassword["width"] = 20
        self.entryPassword.focus_set()
        self.entryPassword.grid(row=1, column=1, padx=10, sticky=E)
        self.entryPassword.insert(0, "")
        #3rd row ******host*******
        self.labelHost = Label(window, text="Host (*):")
        self.labelHost.grid(row=2, column=0, padx=10, pady=2, sticky=W)

        self.entryHost = Entry(window)
        self.entryHost["width"] = 20
        self.entryHost.focus_set()
        self.entryHost.grid(row=2, column=1, padx=10, sticky=E)
        self.entryHost.insert(0, "localhost")
        #4th row *******port******
        self.labelPort = Label(window, text="Port (*):")
        self.labelPort.grid(row=3, column=0, padx=10, pady=2, sticky=W)

        self.entryPort = Entry(window)
        self.entryPort["width"] = 20
        self.entryPort.focus_set()
        self.entryPort.grid(row=3, column=1, padx=10, sticky=E)
        self.entryPort.insert(0, "5432")
        #5th row *******Database Name******
        self.labelDatabaseName = Label(window, text="Database Name (*):")
        self.labelDatabaseName.grid(row=4, column=0, padx=10, pady=2, sticky=W)

        self.entryDatabaseName = Entry(window)
        self.entryDatabaseName["width"] = 20
        self.entryDatabaseName.focus_set()
        self.entryDatabaseName.grid(row=4, column=1, padx=10, sticky=E)
        self.entryDatabaseName.insert(0, "")
        #6th row ******Button******
        self.buttonConnect = ttk.Button(window, text="Connect", command=self.connectDatabase, width=19)
        self.buttonConnect.grid(row=5, column=1, padx=10, pady=10, sticky=E)

        self.schema = None

    def connectDatabase(self):

        username = self.entryUsername.get()
        password = self.entryPassword.get()
        host = self.entryHost.get()
        port = self.entryPort.get()
        db_name = self.entryDatabaseName.get()

        try:
            if not (username and host and port and db_name):
                messagebox.showinfo("Error", "Please enter all required information in order to connect to the database")
            else:
                self.schema = Dbschema(username, password, host, port, db_name)
                self.top.destroy()
        except Exception as ex:
            messagebox.showerror("Error", "Unable to connect to the database: \n" + str(ex))

