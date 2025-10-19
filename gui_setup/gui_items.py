from tkinter import *
from gui_setup import buttons


class Item(object):
    # The Item class takes in text and location to setup an item within the GUI (can consist of a label,
    # entry, button, and/or combobox)
    # @param text is a string and represents the text set to the label of the item
    # @param col is an integer and represents the column the item will start on
    # @param rw is an integer and represents the row the item will start on
    def __init__(self, text, col, rw):
        self.text = text
        self.col = col
        self.rw = rw
        self.txtField = Entry()
        self.button = buttons.Btn(self.col, self.rw, self.text)
        self.cmb = buttons.Combo(self.col + 1, self.rw, self.text)

    def get_txtfield(self):
        #returns the text that is currently in the Entry object of the item
        return str(self.txtField.get())

    def get_btn(self):
        #returns the text that is currently in the button object of the item
        return str(self.button.btn_content())

    def get_cmb(self):
        #returns the text that is currently selected in the combobox object of the item
        return str(self.cmb.get_cmb())

    def insert_default_txtfield(self, text):
        #Sets default text in the Entry object of the item
        #@param text is a string that will be the default text of the Entry object
        self.txtField.insert(0, text)

    def set_output_text(self, value):
        #Sets a provided value into a readonly Entry.
        #@param value will be set into the Entry object as a string
        self.txtField.configure(state='normal')  #must convert to normal state in order to alter
        self.txtField.delete(0, 'end')  #delete current content
        self.txtField.insert(0, value)
        self.txtField.configure(state='readonly')  #change back to read only so user can't alter value

    def item_setup(self, window, pad, txtfield_width, default_text, *args, use_btn=True, use_cmb=False):
        # Sets up an item into the given window with given formatting values. Has the option of using
        # a button, combobox, or neither. Will always create a label and Entry object. Default is to use a button
        # @param window is a tkinter Window object that the item will be added to
        # @param pad is an integer with the padding being equal for x and y
        # @param txtfield_width is an integer that represents the width of the Entry object
        # @param default_text is a string that represents the first text option of a button or combobox
        # @param *args takes in any number of strings to represent the other text options for the button or combobox
        # @param use_btn is a boolean to identify if a button object should be incorporated with the item (default True)
        # @param use_cmb is a boolean to i.d. if a combobox object should be incorporated with the item (default False)
        label = Label(window, text=self.text)
        label.grid(column=self.col, row=self.rw, padx=pad, pady=pad, sticky=E)
        if use_btn:
            #Entry Object
            self.txtField = Entry(window, width=txtfield_width)
            self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E+W)
            #Button Object
            self.button = buttons.Btn(self.col + 2, self.rw, default_text, args)
            self.button.btn_setup(window, pad)
        elif use_cmb:
            #ComboBox Object
            self.cmb = buttons.Combo(self.col + 1, self.rw, default_text, *args)
            self.cmb.combo_setup(window)
        else:
            #Entry Object
            self.txtField = Entry(window, width=txtfield_width)
            self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E + W)

    def output(self, window, pad, txtfield_width):
        #output will setup an item like item_setup but will only produce a label and Entry that is set to readonly
        label = Label(window, text=self.text)
        label.grid(column=self.col, row=self.rw, padx=pad, pady=pad, sticky=E)

        self.txtField = Entry(window, width=txtfield_width)
        self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E + W)
        self.txtField.configure(state='readonly')

    def btn_setup(self, window, pad):
        #used for an item that only needs to setup a button object (no label, entry or combobox)
        #@param window is a tkinter Window that the button will be added to
        #@param pad is an integer that will be the padding (same x and y) to go around the button
        self.button.btn_setup(window, pad)

    # ----
    # The following are for setting test data quickly. Comment them out to get rid of this testing function
    # ----

    def set_input_text(self, text_to_set):
        # Clears the current entry and inserts new text
        self.txtField.delete(0, 'end')
        self.txtField.insert(0, str(text_to_set))

    def set_btn_text(self, text_to_set):
        # Sets the text of the associated button, if it exists
        if hasattr(self, 'button') and hasattr(self.button, 'btn'):
            self.button.btn.configure(text=text_to_set)

    def set_cmb_text(self, text_to_set):
        # Sets the value of the associated combobox, if it exists
        if hasattr(self, 'cmb') and hasattr(self.cmb, 'cmb'):
            self.cmb.cmb.set(text_to_set)