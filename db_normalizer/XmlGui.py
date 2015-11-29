__author__ = 'ASUS'
from tkinter import *
import tkinter.filedialog
import Relation
import xmlReader
import FunctionalDependency
from tkinter import ttk
import os

class XmlGui:
    def __init__(self, master):

        frame = Frame(master,borderwidth=5, relief="sunken")
        frame.grid(column=0, row=0, columnspan=2, rowspan=5)

        self.frame2=frame

        self.labelXmlFile = Label(frame, text="XML File:")
        self.labelXmlFile.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.filelocation = Entry(frame, width=100)
        self.filelocation["width"] = 60
        self.filelocation.focus_set()
        self.filelocation.grid(row=1, column=0, padx=10, sticky=W)

        self.buttonBrowse = Button(frame, text="Browse", command=self.openDirectory, height=2, width=20)
        self.buttonBrowse.grid(row=1, column=1)

        self.buttonProcess = Button(frame, text="Process XML File", command=self.processFile, height=2, width=20)
        self.buttonProcess.grid(row=2, padx=10, pady=10, sticky=W)

        self.labelNormalization = Label(frame, text="Normalization:")
        self.labelNormalization.grid(row=3,padx=10, pady=10, sticky=W)

        self.text1 = Text(frame)
        self.text1.grid(columnspan=2, row=4)

        #root.columnconfigure(0, weight=1)
        #root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=0)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=5)

    def openDirectory(self):
        self.filename = tkinter.filedialog.askopenfilename(title="Open a file...")
        self.filelocation.insert(0, self.filename)

#fonksyionu doldur
    def processFile(self):
        self.file_path = self.filelocation.get()
        self.rxml = xmlReader.XmlReader(self.file_path)
        self.relationList = self.rxml.xmlProcessSchemes()
        for relationObj in self.relationList:
            relationObj.computeNormalForm()
            self.text1.insert(5.0, relationObj.print_report())