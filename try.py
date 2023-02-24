import tkinter as tk
from tkinter import ttk

class CustomFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create a style for the button
        style = ttk.Style()
        style.configure('my.TButton', font=('Helvetica', 12), foreground='#333333', background='#f0f0f0', borderwidth=2, relief='raised')
        
        # Create the button using the custom style
        self.button = ttk.Button(self, text='Click Me', style='my.TButton')
        self.button.pack(padx=10, pady=10)
        
# Create an instance of the custom frame
root = tk.Tk()
frame = CustomFrame(root)
frame.pack()

root.mainloop()
