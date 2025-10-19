from tkinter import *
from gui_setup import window_text


class Window(object):
    # Window class takes in two integers and creates a tkinter window
    # @param x_dim is an integer and represents the size of the window, in pixels, in the X dimension
    # @param y_dim is an integer and represents the size of the window, in pixels, in the Y dimension
    def __init__(self):
        self.window = Tk()  #initiate window in Tkinter

    def window_setup(self, title):
        # Sets up the size, location (center of screen), and title of a window.
        # @param title is a string that represents the title of th window and is passed into
        # the window_text.Title() class object
        window_title = window_text.Title(self.window, title)
        window_title.title_setup()

