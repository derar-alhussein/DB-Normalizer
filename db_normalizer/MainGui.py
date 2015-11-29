from tkinter import *
from tkinter import ttk
from AutomaticGui import AutomaticGui
from ManualGui import ManualGui

class MainGui(ttk.Frame):

    def __init__(self, name='main_gui'):
        ttk.Frame.__init__(self, name=name)

        self.pack(expand=Y, fill=BOTH)
        self.master.title('Database Normalizer - ADB Project')
        self.master.geometry("1150x675+10+10")
        #self.master.wm_state('zoomed')

        self._create_widgets()

    def _create_widgets(self):
        mainPanel = Frame(self, name='demo')
        mainPanel.pack(side=TOP, fill=BOTH, expand=Y)

        # create the notebook
        nb = ttk.Notebook(mainPanel, name='notebook')

        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()

        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)
        self._create_descrip_tab(nb)
        self._create_xml_tab(nb)

        #self._create_disabled_tab(nb)

    def _create_descrip_tab(self, nb):

        automatic = AutomaticGui(nb)
        #frame = ttk.Frame(nb, name='descrip')
        nb.add(automatic._frame, text='Automatic', underline=0, padding=2)

    def _say_neat(self, v):
        v.set('Yeah, I know...')
        self.update()
        self.after(500, v.set(''))

    # =============================================================================
    def _create_xml_tab(self, nb):

        manual = ManualGui(nb)
        #frame = ttk.Frame(nb, name='descrip')
        nb.add(manual._frame, text='Manual', underline=0, padding=2)


    # =============================================================================
    def _create_disabled_tab(self, nb):
        # Populate the second pane. Note that the content doesn't really matter
        frame = ttk.Frame(nb)
        nb.add(frame, text='Disabled', state='disabled')


if __name__ == "__main__":
    MainGui().mainloop()


