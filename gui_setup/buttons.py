from tkinter.ttk import *
import gui_setup.computations
import gui_setup.gui_items


class Btn(object):
    # Btn class takes in two integers, and any number of strings to create a tkinter button
    # @param col is the column location for the button (integer)
    # @param rw is the Item location for the button (integer)
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
        # This function handles the button event. Differentiates between a button click used to determine units of given
        # data and the submit button that starts the calculations.
        if self.btntxt == 'Submit':
            # triggers port tuning computations and sets it to an Entry object
            gui_setup.computations.set_port_tuning_entry()
            # below is for testing purposes
            gui_setup.computations.calculate_and_set_wb()
            gui_setup.computations.calculate_and_set_w()
            gui_setup.computations.calculate_and_set_s()
            gui_setup.computations.calculate_and_set_ccab()
            gui_setup.computations.calculate_and_set_ral()
            gui_setup.computations.calculate_and_set_lmap()
            gui_setup.computations.calculate_and_set_zb()
            #gui_setup.computations.calculate_and_set_pd()
            #gui_setup.computations.calculate_and_set_i()
            #gui_setup.computations.calculate_and_set_u()
            gui_setup.computations.calculate_pd_i_u()
            gui_setup.computations.calculate_zccab()
            gui_setup.computations.calculate_iccab()
            gui_setup.computations.calculate_zlmap()
            gui_setup.computations.calculate_ilmap()
            gui_setup.computations.calculate_port_velocity()
            gui_setup.computations.calculate_cone_excursion()
            gui_setup.computations.calculate_frequency_response()
        if self.clickCount < self.num_args:
            # cycles through given button text if not at end of list
            self.btn.configure(text=self.args[0][self.clickCount])
            self.clickCount += 1
            return
        else:
            # if at the end of the list, button text resets to its default
            self.btn.configure(text=self.btntxt)
            self.clickCount = 0
            return


class Combo(object):
    # Combo class takes in two integers and any number of strings to create a tkinter Combobox
    # @param col is the column location for the Combobox (integer)
    # @param rw is the Item location for the Combobox (integer)
    # @param btntxt is the initial text for the Combobox
    # @param *args is meant to take in the additional text the Combobox can have.
    def __init__(self, col, rw, btntxt, *args):
        self.col = col
        self.rw = rw
        self.args = [btntxt, *args]
        self.num_args = 0
        self.cmb = Combobox()

    def combo_setup(self, window):
        # Sets up the Combobox and adds it to the window at the given location
        # @param window is a tkinter window object that the button will be added to
        self.cmb = Combobox(window, state='readonly')
        self.cmb['values'] = tuple(self.args)
        self.cmb.current(0)
        self.cmb.grid(column=self.col, row=self.rw)

    def get_cmb(self):
        #Returns the current selection in the Combobox
        return self.cmb.get()
