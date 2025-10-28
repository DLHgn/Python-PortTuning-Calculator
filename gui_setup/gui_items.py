from tkinter import *
from gui_setup import buttons
import tkinter.ttk as ttk
import tkinter as tk

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
        self._unit_widget_type = None
        self.button = buttons.Btn(self.col, self.rw, self.text)
        self.cmb = buttons.Combo(self.col + 1, self.rw, self.text)
        self.is_valid = True  # Track validation state
        self.default_bg = None  # Store default background color
        self.min_value = None
        self.max_value = None
        self.error_message = ""

    def validate_numeric_input(self, event=None):
        # Checks if the Entry content is a valid float.
        # Updates highlight border color for errors, otherwise reverts to default.
        # Stores default border settings once.
        if not hasattr(self, 'txtField') or not isinstance(self.txtField, tk.Entry):
            return True  # Not an Entry field, skip validation
        # Now, check if the Entry is read-only
        if self.txtField.cget('state') == 'readonly':
            return True  # Skip validation for read-only fields like Port Tuning

        # Store default border settings (if not already stored)
        # Initialize storage attributes if they don't exist
        if not hasattr(self, 'default_highlight_thickness'):
            self.default_highlight_thickness = None
        if not hasattr(self, 'default_highlight_color'):
            self.default_highlight_color = None

        # Store default thickness once
        if self.default_highlight_thickness is None:
            try:
                # Default thickness is often 0 or 1
                thickness_str = self.txtField.cget("highlightthickness")
                self.default_highlight_thickness = int(thickness_str)
            except:
                self.default_highlight_thickness = 0  # Fallback

        # Store default highlight background color once
        if self.default_highlight_color is None:
            try:
                # This is the color shown when widget doesn't have focus
                self.default_highlight_color = self.txtField.cget("highlightbackground")
                # Ensure it's not empty
                if not self.default_highlight_color: self.default_highlight_color = 'SystemButtonFace'  # A guess
            except:
                self.default_highlight_color = 'SystemButtonFace'  # Fallback color

        current_value_str = self.get_txtfield()
        self.is_valid = False  # Assume invalid until proven otherwise
        self.error_message = ""  # Reset error

        try:
            current_value_float = float(current_value_str)

            # CHECK BOUNDS
            valid_bounds = True
            if self.min_value is not None and current_value_float < self.min_value:
                self.error_message = f"Value must be >= {self.min_value}"
                valid_bounds = False
            elif self.max_value is not None and current_value_float > self.max_value:
                self.error_message = f"Value must be <= {self.max_value}"
                valid_bounds = False

            if valid_bounds:
                # If successful and within bounds, RESET border
                reset_thickness = getattr(self, 'default_highlight_thickness', 0)
                reset_color = getattr(self, 'default_highlight_color', 'SystemButtonFace')
                self.txtField.config(
                    highlightthickness=reset_thickness,
                    highlightbackground=reset_color
                )
                self.is_valid = True
                return True
            else:
                # If out of bounds, set RED border
                self.txtField.config(
                    highlightthickness=2,
                    highlightbackground="red"
                )
                # Keep is_valid = False
                return False

        except ValueError:
            # If float conversion fails, set RED border
            self.error_message = "Invalid numeric input"
            self.txtField.config(
                highlightthickness=2,
                highlightbackground="red"
            )
            # Keep is_valid = False
            return False

    def get_txtfield(self):
        #returns the text that is currently in the Entry object of the item
        return str(self.txtField.get())

    def get_btn(self):
        #returns the text that is currently in the button object of the item
        if hasattr(self, 'button') and self.button:
            return str(self.button.btn_content())  # Make sure it calls the method
        return ""  # Return empty string if button object doesn't exist

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

    def get_current_unit(self):
        unit = None
        widget_type = getattr(self, '_unit_widget_type', None)
        if widget_type == 'button':
            unit = self.get_btn()
        elif widget_type == 'cmb':
            unit = self.get_cmb()
        return unit

    def item_setup(self, window, pad, txtfield_width, default_text, *args, use_btn=True,
                   use_cmb=False, min_value=None, max_value=None):

        label = Label(window, text=self.text)
        label.grid(column=self.col, row=self.rw, padx=pad, pady=pad, sticky=E)
        self.min_value = min_value
        self.max_value = max_value

        if use_btn and not use_cmb:
            self.txtField = Entry(window, width=txtfield_width)
            self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E + W)
            self.txtField.bind("<KeyRelease>", self.validate_numeric_input)
            self.txtField.bind("<FocusOut>", self.validate_numeric_input)
            # --- ENSURE THIS LINE EXISTS ---
            self._unit_widget_type = 'button'
            # -------------------------------
            self.button = buttons.Btn(self.col + 2, self.rw, default_text, args)
            self.button.btn_setup(window, pad)
        elif use_cmb:
            self._unit_widget_type = 'cmb'
            self.txtField = None  # No entry field for combobox items currently
            self.cmb = buttons.Combo(self.col + 1, self.rw, default_text, *args)
            self.cmb.combo_setup(window)
        else:  # Entry only
            self._unit_widget_type = None
            self.txtField = Entry(window, width=txtfield_width)
            self.txtField.grid(column=self.col + 1, row=self.rw, padx=pad, pady=pad, sticky=E + W)
            self.txtField.bind("<KeyRelease>", self.validate_numeric_input)
            self.txtField.bind("<FocusOut>", self.validate_numeric_input)

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
        # Reset validation state after setting programmatically
        self.validate_numeric_input()

    def set_btn_text(self, text_to_set):
        # Sets the text of the associated button, if it exists
        if hasattr(self, 'button') and hasattr(self.button, 'btn'):
            self.button.btn.configure(text=text_to_set)

    def set_cmb_text(self, text_to_set):
        # Sets the value of the associated combobox, if it exists
        if hasattr(self, 'cmb') and hasattr(self.cmb, 'cmb'):
            self.cmb.cmb.set(text_to_set)