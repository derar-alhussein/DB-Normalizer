from tkinter import *
from tkinter import ttk
from tkinter import Listbox
from tkinter import messagebox
from tkinter import filedialog
import Relation
import xmlReader
from FunctionalDependency import FunctionalDependency
from Relation import Relation
from DBSchema import Dbschema
from ConnectionDialog import ConnectionDialog
from Attribute import Attribute
from FdGui import FdGui
from Key import Key

class ManualGui:
    def __init__(self, master):


        frame = Frame(master,borderwidth=5)
        frame.grid(column=0, row=0, columnspan=2, rowspan=5)

        self._frame = frame

        labelframe = LabelFrame(frame, text="Relation Information: ")
        labelframe.grid(row=2, column=2, columnspan=3, ipadx=100, padx=20, pady=5, sticky='wn')

        frm_name = Frame(labelframe)
        frm_name.pack(side='left', anchor='nw', padx=25, pady=10 )
        lbl_name = Label(frm_name, text="Name:")
        lbl_name.pack(anchor='w',pady=3)
        lbl_attributes = Label(frm_name, text="Attributes:")
        lbl_attributes.pack(anchor='w',pady=3)
        lbl_automatic_keys = Label(frm_name, text="Automatically Compute Keys:")
        lbl_automatic_keys.pack( anchor='nw',pady=3)
        lbl_keys = Label(frm_name, text="Keys:")
        lbl_keys.pack(anchor='w',pady=3)
        lbl_fds = Label(frm_name, text="Functional Dependencies:")
        lbl_fds.pack( anchor='nw',pady=2)


        frm_attributes= Frame(labelframe, pady=10)
        frm_attributes.pack(side='left',anchor='w')
        #self.name = Label(frm_attributes, text="-", font = "-weight bold")
        self.entry_name = Entry(frm_attributes, width=100)
        self.entry_name.pack(anchor='w',pady=5)
        self.entry_name.insert(0, "R")
        self.entry_attributes = Entry(frm_attributes, width=100)
        self.entry_attributes.pack( anchor='w',pady=5)
        self.entry_attributes.insert(0, "A, B, C, D, E")
        self.automatic_keys_var = IntVar()
        #self.automatic_keys_var.set(1)
        self.chk_automatic_keys = Checkbutton(frm_attributes, text="",command=self.onChecked, variable =self.automatic_keys_var)
        self.chk_automatic_keys.pack(anchor='w',pady=1)

        self.entry_keys = Entry(frm_attributes, width=100)
        self.entry_keys.pack(anchor='w',pady=5)
        self.entry_keys.insert(0, "A.B, B.C")
        self.entry_fds = Entry(frm_attributes, width=100)
        self.entry_fds.pack(anchor='w')
        self.entry_fds.insert(0, "A.B -> C.D, C -> A.D.E, B -> D.E, D -> E")

        self.compute_normal_form = ttk.Button(frm_attributes, text="Normalize Relation", command=self.compute_normal_form_clicked , width=25)
        self.compute_normal_form.pack(side = 'left', anchor='w',pady=1)
        self.compute_normal_form = ttk.Button(frm_attributes, text="Clear fields", command = self.clear_fields , width=25)
        self.compute_normal_form.pack(anchor='w',pady=1, padx=5)

        nb = ttk.Notebook(frame, name='normalization',height=350,width=870)
        nb.grid(row=3, column=2, columnspan=3, padx=20,pady=10, sticky='wne')
        self._create_report_tab(nb)
        self._create_ddl_tab(nb)
        self._create_dml_tab(nb)
        self._create_drop_ddl_tab(nb)
        #self._create_text_tab(nb)

        self.current_relation = None

        '''
        self.RelationInfo= Label(frame,text="Relation Info:", font=13)
        self.RelationInfo.grid(row=0, sticky=NW)

        self.label_1= Label(frame,text="Name")
        self.label_1.grid(row=2, sticky=E)

        self.label_2= Label(frame,text="Attributes")
        self.label_2.grid(row=3, sticky=E)


        self.label_3= Label(frame,text="Keys")
        self.label_3.grid(row=4, sticky=E)

        self.label_4= Label(frame,text="FDs")
        self.label_4.grid(row=5, sticky=E)

        self.entry_name= Entry(frame,width=50)
        self.entry_name.grid(row=2,column=1)

        self.entry_attributes= Entry(frame,width=50)
        self.entry_attributes.grid(row=3,column=1)

        self.entry_keys= Entry(frame,width=50)
        self.entry_keys.grid(row=4,column=1)

        self.entry_fds= Entry(frame,width=50)
        self.entry_fds.grid(row=5,column=1)

        self.NormResult= Label(frame,text="Normalization Result:", font=15)
        self.NormResult.grid(row=10, sticky=E)

        self.Result= Text (frame,width=60,tabs=10)
        self.Result.grid(row=11,column=1)



        self.buttonBrowse = Button(frame, text="Compute Normal Form", command=self.Naming, height=2, width=20)
        self.buttonBrowse.grid(row=9, column=0)

#        Name = self.entry_1.get()
#       Attributes = self.entry_2.get()
#       Keys = self.entry_3.get()
#       FDs = self.entry_4.get()

#    def printName(self):
#     print("Compute Normal Form")
            '''
    def Naming(self):
        txt_name = self.entry_name.get().replace(" ","")
        txt_attributes = self.entry_attributes.get().replace(" ","")
        txt_keys = self.entry_keys.get().replace(" ","")
        txt_fds = self.entry_fds.get().replace(" ","")

        relationObject = Relation()
        relationObject.Name = txt_name
        relationObject.Attributes = txt_attributes.split(",")



    def processNormForm(self):
            Name = self.entry_1.get()
            Attributes = self.entry_2.get()
            Keys = self.entry_3.get()
            FDs = self.entry_4.get()

    def onChecked(self):
        if self.automatic_keys_var.get():
            messagebox.showinfo("Automatically Compute Keys", "Keys will be automatically computed from the specified FDs.\nIf no key found, the basic key (U->U) will be considered")
            #self.preserve_dependency.config(text='(BCNF is not guarantied)')
            self.entry_keys.config(state=DISABLED)
        else:
            self.entry_keys.config(state=NORMAL)


    def compute_normal_form_clicked(self):
        # Filling FDs from GUI
        try:
            txt_name = self.entry_name.get().replace(" ","")
            txt_attributes = self.entry_attributes.get().replace(" ","")
            txt_keys = self.entry_keys.get().replace(" ","")
            txt_fds = self.entry_fds.get().replace(" ","")

            self.current_relation = Relation()
            self.current_relation.Name = txt_name

            for att in txt_attributes.split(','):
                self.current_relation.Attributes.append(Attribute(att))

            fds_list = []
            for txt_fd in txt_fds.split(','):
                txt_lhs_rhs = txt_fd.split('->')

                lhs_attributes = txt_lhs_rhs[0].split('.')
                rhs_attributes = txt_lhs_rhs[1].split('.')

                fd_object = FunctionalDependency()

                for attribute in lhs_attributes:
                    attribute_object = self.current_relation.Attributes[self.current_relation.Attributes.index(Attribute(attribute))]
                    fd_object.leftHandSide.append(attribute_object)

                for attribute in rhs_attributes:
                    attribute_object = self.current_relation.Attributes[self.current_relation.Attributes.index(Attribute(attribute))]
                    fd_object.rightHandSide.append(attribute_object)

                fds_list.append(fd_object)

                self.current_relation.FDs = fds_list

            if self.automatic_keys_var.get():
                # automatic keys computation
                self.current_relation.compute_candidate_keys()

                keys_str = ''
                for key in self.current_relation.Keys:
                    key_str = ''
                    for attribute in key.Attributes:
                        key_str += attribute.Name + '.'
                    keys_str +=  key_str[:-1] + ", "
                self.entry_keys.insert(0, keys_str)

            else:
                for txt_key in txt_keys.split(","):
                    key_object = Key()
                    for att in txt_key.split("."):
                        key_object.Attributes.append(Attribute(att))
                    self.current_relation.Keys.append(key_object)

            self.current_relation.computeNormalForm()
            self.current_relation.decompose()

            self.txt_result.delete(0.0,END)
            #self.txt_result.insert(5.0, relationObject.Name + ":\n")
            #self.txt_result.insert(5.0, relationObject.NormalForm)
            self.txt_result.insert(0.0, self.current_relation.print_report())

            self.txt_ddl.delete(0.0,END)
            self.txt_ddl.insert(0.0, str(self.current_relation.buildCreateTableScript()))

            self.txt_dml.delete(0.0,END)
            self.txt_dml.insert(0.0, str(self.current_relation.buildDmlScript()))

            self.txt_ddl_drop.delete(0.0,END)
            self.txt_ddl_drop.insert(0.0, str(self.current_relation.buildDropTableClause()))


        except Exception as ex:
            messagebox.showerror("Error", "An error occurred during normalization.\n Please, make sure that all fields are in correct format")

    def _create_report_tab(self, nb):
       # frame to hold contentx
        frame2 = ttk.Frame(nb, name='report')

        frame = ttk.Frame(frame2)
        frame.pack(fill=BOTH, expand=Y, padx=10, pady=10)
        self.txt_result = Text(frame, wrap=WORD, width=40, height=10)
        vscroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.txt_result.yview)
        self.txt_result['yscroll'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        self.txt_result.pack(fill=BOTH, expand=Y)


        self.btn_export_xml = ttk.Button(frame2, text='Export to XML', underline=0, command=self.btn_export_xml_clicked)
        self.btn_export_xml.pack(side='left',padx=10, pady=10,anchor='sw')

        # add to notebook (underline = index for short-cut character)
        nb.add(frame2, text='Normalization Proposal', underline=0, padding=2)

    def _create_ddl_tab(self, nb):
        # frame to hold contentx
        frame2 = ttk.Frame(nb, name='ddl')

        frame = ttk.Frame(frame2)
        frame.pack(fill=BOTH, expand=Y, padx=10, pady=10)
        self.txt_ddl = Text(frame, wrap=WORD, width=40, height=10)
        vscroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.txt_ddl.yview)
        self.txt_ddl['yscroll'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        self.txt_ddl.pack(fill=BOTH, expand=Y)

        btn_save_ddl = ttk.Button(frame2, text='Save', underline=0 , command=self.btn_save_ddl_clicked)
        btn_save_ddl.pack(side='left',padx=10, pady=10,anchor='sw')

        # add to notebook (underline = index for short-cut character)
        nb.add(frame2, text='DDL: Create New Tables', underline=0, padding=2)

    def _create_dml_tab(self, nb):
        # frame to hold contentx
        frame2 = ttk.Frame(nb, name='dml')

        frame = ttk.Frame(frame2)
        frame.pack(fill=BOTH, expand=Y, padx=10, pady=10)
        self.txt_dml = Text(frame, wrap=WORD, width=40, height=10)
        vscroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.txt_dml.yview)
        self.txt_dml['yscroll'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        self.txt_dml.pack(fill=BOTH, expand=Y)

        btn_save_dml = ttk.Button(frame2, text='Save', underline=0, command=self.btn_save_dml_clicked)
        btn_save_dml.pack(side='left',padx=10, pady=10,anchor='sw')

        # add to notebook (underline = index for short-cut character)
        nb.add(frame2, text='DML: Data Migration', underline=0, padding=2)

    def _create_drop_ddl_tab(self, nb):
        # frame to hold contentx
        frame2 = ttk.Frame(nb, name='drop_ddl')

        frame = ttk.Frame(frame2)
        frame.pack(fill=BOTH, expand=Y, padx=10, pady=10)
        self.txt_ddl_drop = Text(frame, wrap=WORD, width=40, height=10)
        vscroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.txt_ddl_drop.yview)
        self.txt_ddl_drop['yscroll'] = vscroll.set
        vscroll.pack(side=RIGHT, fill=Y)
        self.txt_ddl_drop.pack(fill=BOTH, expand=Y)

        btn_save_ddl_drop = ttk.Button(frame2, text='Save', underline=0, command = self.btn_save_ddl_drop_clicked)
        btn_save_ddl_drop.pack(side='left',padx=10, pady=10,anchor='sw')

        # add to notebook (underline = index for short-cut character)
        nb.add(frame2, text='DDL: Drop Old Tables', underline=0, padding=2)

    def btn_export_xml_clicked(self):
        if self.current_relation:
            f = filedialog.asksaveasfilename(title="Export to XML...", defaultextension=".xml")
            if f == '':
                return
            rxml = xmlReader.XmlReader('schema.xml')
            rxml.xmlCompleteStructure([self.current_relation], f)

    def btn_save_ddl_clicked(self):
        script = str(self.txt_ddl.get(1.0, END))
        self.save_file( script)

    def btn_save_dml_clicked(self):
        script = str(self.txt_dml.get(1.0, END))
        self.save_file( script)

    def btn_save_ddl_drop_clicked(self):
        script = str(self.txt_ddl_drop.get(1.0, END))
        self.save_file(script)

    def save_file(self, text2save):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".sql")
        if f is None:
            return
        f.write(text2save)
        f.close()

    def clear_fields(self):
        self.entry_name.delete(0, END)
        self.entry_attributes.delete(0, END)
        self.entry_fds.delete(0, END)
        self.automatic_keys_var.set(0)
        self.entry_keys.config(state=NORMAL)
        self.entry_keys.delete(0, END)