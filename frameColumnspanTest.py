from tkinter import *
#from main import next_card
import tkinter as tk
import subprocess
import csv

k=1
m=k+2
def add_frames_from_csv(root):
    
    with open("data.csv") as f:
        reader = csv.reader(f)
        i=1
        global k
        for row in reader:
            if len(row)>0:#41B77F, width=120, height=100
              info_frame =tk.Frame(root)
              info_frame.grid(row= k, column=i, padx=20, pady=20 )
              info_frame.config(bg='#050D54')
              button=Button(info_frame, text=row[2], font=("Courrier", 25),cursor='hand2', height=4, width=19, bg=row[3], fg='white', command=run_python_script)
              button.grid(row=0, column=0, pady=0,  padx=0, columnspan=10, sticky="ne")
              button11=Button(info_frame,image=image_ajout1,borderwidth=0, cursor='hand2', command=add_button)
              button11.grid(pady=1, padx=1, row=2, column=3,sticky="w")
              button12=Button(info_frame,image=image_ajout2,borderwidth=0, cursor='hand2', command=add_button)
              button12.grid(pady=1, padx=1, row=2, column=4, sticky="w")
              button13=Button(info_frame,image=image_ajout3,borderwidth=0, cursor='hand2', command=add_button)
              button13.grid(pady=1, padx=1, row=2, column=5, sticky="w")
              button14=Button(info_frame,image=image_ajout4,borderwidth=0, cursor='hand2', command=add_button)
              button14.grid(pady=1, padx=1, row=2, column=6, sticky="w")
              button15=Button(info_frame,image=image_ajout5,borderwidth=0, cursor='hand2', command=add_button)
              button15.grid(pady=1, padx=1, row=2, column=7, sticky="w")
              i+=1
              if i%3==0:
                i=0
                k+=1


def run_game_script():
    subprocess.call(["python", "hangman.py"])

def run_graph_script():
    subprocess.call(["python", "graph.py"])

def run_python_script():
    subprocess.call(["python", "main1.py"])

def add_button():
    subprocess.call(["python", "enterInfoFlashCard.py"])


root=Tk()
root.title('flashcard App')
root.config(background='#050D54')

image_ajt=PhotoImage(file="logo.png")
label1= Label(root, image=image_ajt, borderwidth=0)
label1.grid(padx=0,row=0, column=0, columnspan=4, sticky="w")
label1= Label(root, text="FlashCards",font=("courrier", 40, 'bold'), bg='#050D54', fg='#38ADFC')
label1.grid(padx=0,pady=18,row=0, column=0, sticky="ne")

#principalFrame
frame = tk.Frame(root)
frame.config(bg='#050D54')
frame.grid(row=1, column=0,padx=20,pady=0)

button=Button(frame, text='frToEng', font=("Courrier", 25),bg='#FAD727' , fg='white', height=4, width=19, command=run_python_script)
button.grid(row=1, column=0, pady=0, padx=10, columnspan=10, sticky="ne")

image_ajout1=PhotoImage(file="addCard.png")
image_ajout2=PhotoImage(file="edit.png")
image_ajout3=PhotoImage(file="graph.png")
image_ajout4=PhotoImage(file="game.png")
image_ajout5=PhotoImage(file="trash.png")

button6=Button(frame,image=image_ajout1,borderwidth=0, cursor='hand2', command=add_button)
button6.grid(pady=1, padx=1, row=2, column=3,sticky="w")
button7=Button(frame,image=image_ajout2,borderwidth=0, cursor='hand2', command=add_button)
button7.grid(pady=1, padx=1, row=2, column=4, sticky="w")
button8=Button(frame,image=image_ajout3,borderwidth=0, cursor='hand2', command=run_graph_script)
button8.grid(pady=1, padx=1, row=2, column=5, sticky="w")
button9=Button(frame,image=image_ajout4,borderwidth=0, cursor='hand2', command=run_game_script)
button9.grid(pady=1, padx=1, row=2, column=6, sticky="w")
button10=Button(frame,image=image_ajout5,borderwidth=0, cursor='hand2', command=add_button)
button10.grid(pady=1, padx=1, row=2, column=7, sticky="w")

add_frames_from_csv(root)

image_ajout=PhotoImage(file="add.png")
#image_ajout = image_ajout.subsample(2, 2)relief="raised", bd=0 
button =Button(root,image=image_ajout,width=60,bg='white',height=60, borderwidth=0, cursor='hand2', border='0', command=add_button)
button.config()
button.grid(pady=10, padx=10, row=3, column=2)
#output_button = Button(root, text="Return Output", command=return_output)
#output_button.grid(row=2, column=0)



root.mainloop()