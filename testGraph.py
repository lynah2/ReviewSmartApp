import tkinter as tk
text1='khadija'
def my_function(text1):
    # This function will be executed when the button is clicked
    print("Button clicked!")
    window = tk.Tk()

    # create a label
    label = tk.Label(window, text="Hello, world!" + text1)

    # add the label to the window
    label.pack()

    # run the tkinter event loops
    window.mainloop()

# Create a tkinter window
window = tk.Tk()

# Create a button and add it to the window
button = tk.Button(window, text="Click me",  command=lambda: my_function(text1))
button.pack()

# Run the tkinter event loop
window.mainloop()
