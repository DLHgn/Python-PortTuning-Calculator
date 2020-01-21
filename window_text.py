class Title(object):
    # Title class is designed to take in two arguments (window and text) and set the title of a given window.
    # @param window is the tkinter window to be acted on.
    # @param text is a string variable and is set as the title of the window argument that is passed.
    def __init__(self, window, text):
        self.window = window
        self.text = text

    def title_setup(self):
        self.window.title(self.text)
