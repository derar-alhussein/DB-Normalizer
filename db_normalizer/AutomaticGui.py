__author__ = 'ASUS'
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
import copy

class AutomaticGui:
    def __init__(self, master):

        #frame = Frame(master, borderwidth=5, height=640, width=480)
        frame = Frame(master, borderwidth=5)
        frame.grid(column=0, row=0)
        self._frame = frame
        self.root =master

        frm_db = Frame(frame)
        frm_db.grid(row=0, column=0, padx=10, pady=5, sticky=NW)

        lbl_db = Label(frm_db, text="Import from Database:")
        lbl_db.pack(anchor='w',pady=1)

        # Connect Button
        self.buttonConnectDb = ttk.Button(frm_db, text="Connect to Database", command=self.openDbConnectionWindow, width=25)
        self.buttonConnectDb.pack(anchor='w',pady=1)

        self.separator2 = ttk.Separator(frame, orient='vertical')
        self.separator2.grid(row=0, column=1,sticky=NS)



        frm_xml = Frame(frame)
        frm_xml.grid(row=0, column=2, padx=10, sticky=W)

        lbl_xml = Label(frm_xml, text="Import from XML:")
        lbl_xml.pack(anchor='w',pady=1)

        lbl_xml = Label(frm_xml, text="XML file:")
        lbl_xml.pack(side='left',anchor='w',pady=1)

        self.filelocation = Entry(frm_xml, width = 100)
        self.filelocation.focus_set()
        self.filelocation.pack(side='left', anchor='w',padx=8,pady=1)

        self.btn_browse_xml = ttk.Button(frm_xml, text="Browse", command=self.btn_browse_xml_clicked, width=25)
        self.btn_browse_xml.pack(anchor='w',pady=1)

        self.separator2 = ttk.Separator(frame, orient=HORIZONTAL)
        self.separator2.grid(row=1, columnspan=5, pady=10,  sticky=EW)

        # Treeview:
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set, height=25)
        self.tree.heading('#0', text='Tables', anchor='w')
        self.tree.bind("<Button-1>", self.onClick)

        self.tree.grid(row=2, column=0, rowspan=2)
        ysb.grid(row=2, column=1, sticky='ns', rowspan=2)
        xsb.grid(row=4, column=0, sticky='ew')

        # Labels
        labelframe = LabelFrame(frame, text="Relation Information: ")
        labelframe.grid(row=2, column=2, columnspan=3, ipadx=20, padx=20, pady=5, sticky='wn')

        frm_name = Frame(labelframe)
        frm_name.pack(side='left', anchor='nw', padx=25, pady=10 )
        lbl_name = Label(frm_name, text="Name:")
        lbl_name.pack(anchor='w',pady=1)
        lbl_attributes = Label(frm_name, text="Attributes:")
        lbl_attributes.pack(anchor='w',pady=1)
        lbl_keys = Label(frm_name, text="Keys:")
        lbl_keys.pack(anchor='w',pady=1)
        lbl_fds = Label(frm_name, text="Functional Dependencies:")
        lbl_fds.pack( anchor='nw',pady=4)
        lbl_automatic_keys = Label(frm_name, text="Automatically Compute Keys:")
        lbl_automatic_keys.pack( anchor='nw',pady=1)

        frm_attributes= Frame(labelframe, pady=10)
        frm_attributes.pack(side='left',anchor='w')
        #self.name = Label(frm_attributes, text="-", font = "-weight bold")
        self.name = Label(frm_attributes, text="-")
        self.name.pack(anchor='w',pady=1)
        self.attributes = Label(frm_attributes, text="-")
        self.attributes.pack( anchor='w',pady=1)
        self.keys = Label(frm_attributes, text="-")
        self.keys.pack(anchor='w',pady=1)

        frm_attributes2= Frame(frm_attributes)
        frm_attributes2.pack(anchor='w')
        self.entry_fds = Entry(frm_attributes2, width=75)
        self.entry_fds.config(state=DISABLED)
        self.entry_fds.pack(side='left' ,anchor='sw',pady=3)
        self.specify_fds = ttk.Button(frm_attributes2, text="Specify & Test FDs", command=self.add_fds , width=25)
        self.specify_fds.state(["disabled"])
        self.specify_fds.pack(anchor='sw',padx = 10, pady=1)

        self.automatic_keys_var = IntVar()
        #self.automatic_keys_var.set(1)
        self.chk_automatic_keys = Checkbutton(frm_attributes, text="",command=self.onChecked, variable =self.automatic_keys_var)
        self.chk_automatic_keys.pack(anchor='w',pady=1)
        self.compute_normal_form = ttk.Button(frm_attributes, text="Normalize Relation", command=self.compute_normal_form_clicked , width=25)
        self.compute_normal_form.state(["disabled"])
        self.compute_normal_form.pack(anchor='w',pady=1)

        nb = ttk.Notebook(frame, name='normalization',height=280,width=870)
        nb.grid(row=3, column=2, columnspan=3, padx=20,pady=10, sticky='wne')
        self._create_report_tab(nb)
        self._create_ddl_tab(nb)
        self._create_dml_tab(nb)
        self._create_drop_ddl_tab(nb)
        #self._create_text_tab(nb)

        self.current_relation = None
        self.schema = None
        #self.textResult = Text(frame)
        #self.textResult.grid(row=0, column=2, padx=10)

    def add_fds(self):
        str_name = self.name['text']
        if str_name != '-':
            realtion_object = self.relationList[self.relationList.index(Relation(str_name))]

        fd_gui = FdGui(self.root, self.entry_fds,realtion_object, self.schema)
        self.root.wait_window(fd_gui.top)

    def onChecked(self):
        if self.automatic_keys_var.get():
            messagebox.showinfo("Automatically Compute Keys", "Keys will be automatically computed from the specified FDs.\nIf no key found, the basic key (U->U) will be considered")
            #self.preserve_dependency.config(text='(BCNF is not guarantied)')

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
        self.btn_export_xml.state(["disabled"])

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

        self.btn_execute_ddl = ttk.Button(frame2, text='Execute', underline=0,  command=self.btn_execute_ddl_clicked)
        self.btn_execute_ddl.pack(pady=10, anchor='sw')

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

        self.btn_execute_dml = ttk.Button(frame2, text='Execute', underline=0, command = self.btn_execute_dml_clicked)
        self.btn_execute_dml.pack(pady=10, anchor='sw')

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

        self.btn_execute_ddl_drop = ttk.Button(frame2, text='Execute', underline=0, command = self.btn_execute_ddl_drop_clicked)
        self.btn_execute_ddl_drop.pack(pady=10, anchor='sw')

        # add to notebook (underline = index for short-cut character)
        nb.add(frame2, text='DDL: Drop Old Tables', underline=0, padding=2)

    def onClick(self, event):
        item = self.tree.identify('item', event.x, event.y)

        if "ROOT" in self.tree.item(item, "value"):
            #self.tree.item(item, open=True)
            columns = self.tree.get_children(item)[0]
            keys = self.tree.get_children(item)[1]

            str_name = self.tree.item(item, "text")

            self.current_relation = copy.deepcopy(self.relationList[self.relationList.index(Relation(str_name))])

            self.name['text'] = self.current_relation

            attributes_str = ''
            for column in self.current_relation.Attributes:
                attributes_str += column.Name + ", "
            self.attributes['text'] = attributes_str[:-2]

            keys_str = ''
            for key in self.current_relation.Keys:
                key_str = ''
                for attribute in key.Attributes:
                    key_str += attribute.Name + '.'
                keys_str +=  key_str[:-1] + ", "
            self.keys['text'] = keys_str[:-2]

            fds_str = ''
            for fd in self.current_relation.FDs:
                fds_str += str(fd) + ', '
            fds_str = fds_str[:-2]
            self.entry_fds.config(state=NORMAL)
            self.entry_fds.delete(0,END)
            self.entry_fds.insert(0, fds_str)

            if len(self.current_relation.Keys) == 0:
                self.automatic_keys_var.set(1)
                self.chk_automatic_keys.configure(state = "disabled")
            else:
                self.chk_automatic_keys.configure(state = "normal")
                self.automatic_keys_var.set(0)

            '''

            #self.entry_fds.delete(0.0, END)

            '''

            self.compute_normal_form.state(["!disabled"])
            self.btn_export_xml.state(["!disabled"])
            self.specify_fds.state(["!disabled"])

            #self.entry_fds.insert(0, 'A.B -> C.D, C -> A.D.E, B -> D.E, D -> E')

    def openDbConnectionWindow(self):
        conn = ConnectionDialog(self.root)
        self.root.wait_window(conn.top)
        if conn.schema:
            self.schema = conn.schema
            self.relationList = self.schema.dbProcessSchemes()
            self.filelocation.delete(0,END)
            self.clear_fields()
            self.enable_execute_fields()
            self.fill_treeview()

    def compute_normal_form_clicked(self):
        str_name = self.name['text']
        if str_name != '-':

            self.current_relation = copy.deepcopy(self.relationList[self.relationList.index(Relation(str_name))])
            # Filling FDs from GUI
            try:
                txt_fds = self.entry_fds.get().replace(" ","")
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
            except:
                messagebox.showinfo("Normal Form Computation", "Empty or Incorrect format of functional dependencies")
                return

            print(self.current_relation.FDs)
            try:
                keys_str = ''
                # automatic keys computation
                if self.automatic_keys_var.get():
                    self.current_relation.compute_candidate_keys()
                    keys_str = 'Automatically Computed :: '

                for key in self.current_relation.Keys:
                    key_str = ''
                    for attribute in key.Attributes:
                        key_str += attribute.Name + '.'
                    keys_str +=  key_str[:-1] + ", "
                self.keys['text'] = keys_str[:-2]

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
                messagebox.showerror("Error", "An error occurred during normalization: \n" + str(ex))
        else:
            messagebox.showinfo("Normal Form Computation", "Please select a relation from the left-side list.")

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

    def btn_execute_ddl_clicked(self):
        script = str(self.txt_ddl.get(1.0, END))
        self.execute_script(script)

    def btn_execute_dml_clicked(self):
        script = str(self.txt_dml.get(1.0, END))
        self.execute_script(script)

    def btn_execute_ddl_drop_clicked(self):
        script = str(self.txt_ddl_drop.get(1.0, END))
        self.execute_script(script)

    def execute_script(self, script):
        try:
            self.schema.execute_script(script)
            #self.fill_treeview()
            messagebox.showinfo("Script Execution", "Script successfully executed")
        except Exception as ex:
            messagebox.showerror("Error", "An error occurred during executing the script: \n" + str(ex))

    def fill_treeview(self):
        # clean treeview old content
        self.tree.delete(*self.tree.get_children())

        for relationObj in self.relationList:
            name_node = self.tree.insert("", "end", text=relationObj.Name, value="ROOT", open=False )


            columns_node = self.tree.insert(name_node, "end", text="Columns:", open=False)
            for attribute in relationObj.Attributes:
                self.tree.insert(columns_node, "end", text=attribute)

            keys_node = self.tree.insert(name_node,"end", text="Keys:", open=False)
            for key in relationObj.Keys:
                self.tree.insert(keys_node, "end", text=key.Attributes)

    def btn_browse_xml_clicked(self):
        try:
            self.filename = filedialog.askopenfilename(title="Open a file...")
            if self.filename != '':
                self.rxml = xmlReader.XmlReader(self.filename)
                self.relationList = self.rxml.xmlProcessSchemes()
                self.filelocation.delete(0,END)
                self.filelocation.insert(0, self.filename)
                self.clear_fields()
                self.disable_execute_fields()
                self.fill_treeview()
        except Exception as ex:
                messagebox.showerror("Error", "An error occurred during file processing: \n" + str(ex))

    def clear_fields(self):
        self.name['text'] = '-'
        self.attributes['text'] = '-'
        self.keys['text'] = '-'
        self.entry_fds.delete(0, END)
        self.entry_fds.config(state=DISABLED)
        self.specify_fds.state(["disabled"])
        self.automatic_keys_var.set(0)
        self.txt_result.delete(0.0,END)
        self.txt_ddl.delete(0.0,END)
        self.txt_dml.delete(0.0,END)
        self.txt_ddl_drop.delete(0.0,END)


    def disable_execute_fields(self):
        self.btn_execute_ddl.state(["disabled"])
        self.btn_execute_dml.state(["disabled"])
        self.btn_execute_ddl_drop.state(["disabled"])

    def enable_execute_fields(self):
        self.btn_execute_ddl.state(["!disabled"])
        self.btn_execute_dml.state(["!disabled"])
        self.btn_execute_ddl_drop.state(["!disabled"])
