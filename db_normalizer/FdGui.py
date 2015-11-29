__author__ = 'Derar'
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import Relation
import xmlReader
from FunctionalDependency import FunctionalDependency
from Relation import Relation
from DBSchema import Dbschema

class FdGui():
    def __init__(self,parent, entry_fds, relationObject, schema):

        window = self.top = Toplevel(parent)
        window.transient(parent)
        #window.grab_set()
        window.title("Functional Dependency")
        window.geometry("360x250+30+30")

        self.entry_fds = entry_fds
        self.relationObject = relationObject
        self.schema = schema

        lbl_lhs = Label(window, text="Left hand side:")
        lbl_lhs.grid(row=0, column=0, columnspan=2)

        lbl_arrow = Label(window, text="->")
        lbl_arrow.grid(row=0, column=2, sticky='w')

        lbl_rhs = Label(window, text="Right hand side:")
        lbl_rhs.grid(row=0, column=3,columnspan=2)

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        self.lb_lhs = Listbox(window, width=25, height=10, yscrollcommand=scrollbar.set, selectmode=MULTIPLE,exportselection=0 )
        scrollbar.config(command=self.lb_lhs.yview)

        #scrollbar.pack(side="right", fill="y")
        #lb_lhs.pack(side="left",anchor='w',expand=True)


        self.lb_lhs.grid(row=1, column=0)
        scrollbar.grid(row=1, column=1, sticky='ns')

        scrollbar2 = ttk.Scrollbar(window, orient="vertical")
        self.lb_rhs = Listbox(window, width=25, height=10, yscrollcommand=scrollbar2.set, selectmode=MULTIPLE,exportselection=0 )
        scrollbar2.config(command=self.lb_rhs.yview)

        self.lb_rhs.grid(row=1, column=3)
        scrollbar2.grid(row=1, column=4, sticky='ns')

        self.add_fd = ttk.Button(window, text="Add FD", command=self.add_fd , width=25)
        #self.compute_normal_form.state(["disabled"])
        self.add_fd.grid(row=2, column=0,pady=20,columnspan=5)

        #scrollbar2.pack(side="right", fill="y")
        #lb_rhs.pack( anchor='w', expand=True)

        for att in self.relationObject.Attributes:
            self.lb_lhs.insert("end", att)
            self.lb_rhs.insert("end", att)

    def add_fd(self):
        if len(self.lb_lhs.curselection())==0 or len(self.lb_lhs.curselection())==0:
            return

        if len(self.entry_fds.get())==0:
            fd = ''
        else:
            fd = ', '
        items_lhs = self.lb_lhs.curselection()
        items_lhs = [self.relationObject.Attributes[int(item)] for item in items_lhs]
        for item in items_lhs:
            fd += str(item) + '.'

        fd = fd[:-1] + ' -> '

        items_rhs = self.lb_rhs.curselection()
        items_rhs = [self.relationObject.Attributes[int(item)] for item in items_rhs]

        for item in items_rhs:
            fd += str(item) + '.'

        is_valid_fd = True

        # testing FD
        if self.schema:
            try:
                fd_object = FunctionalDependency()
                fd_object.leftHandSide = items_lhs
                fd_object.rightHandSide = items_rhs
                is_valid_fd = fd_object.is_valid(self.relationObject, self.schema)
                if is_valid_fd:
                    messagebox.showinfo("FD Testing", "Valid FD")
                else:
                    messagebox.showerror("FD Testing", "Invalid FD !!")

            except Exception as ex:
                messagebox.showerror("Error", "An error occurred during FD testing: \n" + str(ex))

        if is_valid_fd: # valid
            self.entry_fds.insert("end",fd[:-1])

            self.lb_lhs.selection_clear(0,len(self.relationObject.Attributes)-1)
            self.lb_rhs.selection_clear(0,len(self.relationObject.Attributes)-1)

