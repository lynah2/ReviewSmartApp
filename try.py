import tkinter as tk

root = tk.Tk()

text = tk.Text(root, state="disabled")
text.pack()

# Insert text with bullets
text.insert(tk.END, "\u2022 Bullet point 1\n")
text.insert(tk.END, "\u2022 Bullet point 2\n")
text.insert(tk.END, "\u2022 Bullet point 3\n")

root.mainloop()

