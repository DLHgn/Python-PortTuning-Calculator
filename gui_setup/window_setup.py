from tkinter import *
from gui_setup import window_text


class Window(object):
    # Window class takes in two integers and creates a tkinter window
    # @param x_dim is an integer and represents the size of the window, in pixels, in the X dimension
    # @param y_dim is an integer and represents the size of the window, in pixels, in the Y dimension
    def __init__(self, x_dim, y_dim):
        self.x_dim = int(x_dim)  #X Dimension of window
        self.y_dim = int(y_dim)  #Y Dimension of window
        self.window = Tk()  #initiate window in Tkinter

    def window_setup(self, title):
        # Sets up the size, location (center of screen), and title of a window.
        # @param title is a string that represents the title of th window and is passed into
        #        the window_text.Title() class object
        self.window.geometry('%dx%d%s' % (self.x_dim, self.y_dim, self.window_center()))
        window_title = window_text.Title(self.window, title)
        window_title.title_setup()

    def window_center(self):
        # Finds the coordinates to center based on the top left most pixel of the window
        # Returns the coordinates in string format "+x_coordinate+y_coordinate" which is the required syntax of the
        # .geometry() method called on tkinter windows.
        window_width = self.x_dim
        window_height = self.y_dim

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))  #find center X given window and screen Dimensions
        y_coordinate = int((screen_height / 2) - (window_height / 2))  #find center Y given window and screen Dimensions

        return "+%s+%s" % (x_coordinate, y_coordinate)  #return a string already formated to be used in .geometry
