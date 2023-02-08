from tkinter import *
#from main import next_card
import tkinter as tk
import subprocess
import csv

def add_frames_from_csv(root):
    with open("data.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)>0:
              button=Button(root, text=row[0], font=("Courrier", 25), bg='white', fg='#41B77F', command=run_python_script)
              button.pack(pady=25, fill=X)
        


def run_python_script():
    subprocess.call(["python", "main.py"])

def add_button():
    subprocess.call(["python", "enterInfoFlashCard.py"])


#def return_output():
#    return next_card


#def afficher():
  

root=Tk()
root.title('flashcard App')
root.config(background='#41B77F')

label1= Label(root, text="flashCard",font=("courrier", 25), bg='white', fg='#41B77F')
label1.pack()

button=Button(root, text='frToEng', font=("Courrier", 25), bg='white', fg='#41B77F', command=run_python_script)
button.pack(pady=25, fill=X)

add_frames_from_csv(root)

image_ajout=PhotoImage(file="add.png")
button =Button(root,image=image_ajout, command=add_button)
button.config(width=image_ajout.width(), height=image_ajout.height())
button.pack(pady=60, padx=60)
#output_button = Button(root, text="Return Output", command=return_output)
#output_button.grid(row=2, column=0)



root.mainloop()