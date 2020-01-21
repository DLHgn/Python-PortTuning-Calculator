from tkinter.ttk import *
import gui_setup.computations
import gui_setup.gui_items


class Btn(object):
    # Btn class takes in two integers, and any number of strings to create a tkinter button
    # @param col is the column location for the button (integer)
    # @param rw is the Row location for the button (integer)
    # @param btntxt is the initial text for the button
    # @param *args is meant to take in the additional text the button can have (button cycles through given text.
    def __init__(self, col, rw, btntxt, *args):
        self.col = col
        self.rw = rw
        self.btntxt = btntxt
        self.args = args
        if self.args:
            self.num_args = len(self.args[0])
        else:
            self.num_args = 0
        self.btn = Button()
        self.clickCount = 0

    def btn_content(self):
        #returns current text on button
        return self.btn.cget('text')

    def btn_setup(self, window, pad):
        #Sets up the button and adds it to the window at the given location
        # @param window is a tkinter window object that the button will be added to
        # @param pad is the padding used for this button (same pad for x and y to keep it even)
        self.btn = Button(window, text=self.btntxt, command=self.clicked)
        self.btn.grid(column=self.col, row=self.rw, padx=pad, pady=pad)

    def clicked(self):
        #This function handles the button event. Differentiates between a button click used to determine units of given
        #data and the submit button that starts the calculations.
        if self.btntxt == 'Submit':
            gui_setup.computations.set_port_tuning_entry()  #triggers port tuning computations and sets it to an Entry object
        if self.clickCount < self.num_args:
            self.btn.configure(text=self.args[0][self.clickCount])  #cycles through given button text if not at end of list
            self.clickCount += 1
            return
        else:
            self.btn.configure(text=self.btntxt)  #if at the end of the list, button text resets to its default
            self.clickCount = 0
            return


class Combo(object):
    # Combo class takes in two integers and any number of strings to create a tkinter Combobox
    # @param col is the column location for the Combobox (integer)
    # @param rw is the Row location for the Combobox (integer)
    # @param btntxt is the initial text for the Combobox
    # @param *args is meant to take in the additional text the Combobox can have.
    def __init__(self, col, rw, btntxt, *args):
        self.col = col
        self.rw = rw
        self.args = [btntxt, *args]
        self.num_args = 0
        self.cmb = Combobox()

    def combo_setup(self, window):
        #Sets up the 
        self.cmb = Combobox(window, state='readonly')
        self.cmb['values'] = tuple(self.args)
        self.cmb.current(0)
        self.cmb.grid(column=self.col, row=self.rw)

    def get_cmb(self):
        return self.cmb.get()
