from tkinter import *
from gui_setup import buttons


class Row(object):
    def __init__(self, text, col, rw):
        self.text = text
        self.col = col
        self.rw = rw
        self.txtField = Entry()
        self.button = buttons.Btn(self.col, self.rw, self.text)
        self.cmb = buttons.Combo(self.col + 1, self.rw, self.text)

    def get_txtfield(self):
        return str(self.txtField.get())

    def get_btn(self):
        return str(self.button.btn_content())

    def get_cmb(self):
        return str(self.cmb.get_cmb())

    def insert_default_txtfield(self, text):
        self.txtField.insert(0, text)

    def set_tuning(self, value):
        self.txtField.configure(state='normal')
        self.txtField.delete(0, END)
        self.txtField.insert(0, round(value, 2))
        self.txtField.configure(state='readonly')

    def row_setup(self, window, pad, txtfield_width, btn_name, *args, use_btn=True, use_cmb=False):
        #Txt
        label = Label(window, text=self.text)
        label.grid(column=self.col, row=self.rw, padx=pad, pady=pad, sticky=E)
        #Unit Button
        if use_btn:
            # TxtField
            self.txtField = Entry(window, width=txtfield_width)
            self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E+W)
            # Unit Button
            self.button = buttons.Btn(self.col + 2, self.rw, btn_name, args)
            self.button.btn_setup(window, pad)
        elif use_cmb:
            #Combo Box
            self.cmb = buttons.Combo(self.col + 1, self.rw, btn_name, *args)
            self.cmb.combo_setup(window)
        else:
            # TxtField
            self.txtField = Entry(window, width=txtfield_width)
            self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E + W)

    def output(self, window, pad, txtfield_width):
        label = Label(window, text=self.text)
        label.grid(column=self.col, row=self.rw, padx=pad, pady=pad, sticky=E)

        self.txtField = Entry(window, width=txtfield_width)
        self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E + W)
        self.txtField.configure(state='readonly')

    def btn_setup(self, window, pad):
        self.button.btn_setup(window, pad)
