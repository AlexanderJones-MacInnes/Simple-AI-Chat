import FreeSimpleGUI as gui

class Window:
    def __init__(self, title):
        self.event = None
        self.values = None
        self.window = gui.Window(title, self.layout)
    def DisplayWindow(self):
        self.event, self.values = self.window.read()

class ConfirmationBox(Window):
    def __init__(self, title, text):
        self.layout = [
            [gui.Text(text,key = "text")],
            [gui.Button("Yes"), gui.Button("No")]
        ]
        Window.__init__(self, title)

class TextBox(Window):
    def __init__(self, title, text = ""):
        self.layout = [
            [gui.Text(text)],
            [gui.Input(key = "input")],
            [gui.Button("Enter"), gui.Button("Cancel")]
        ]
        Window.__init__(self,title)



