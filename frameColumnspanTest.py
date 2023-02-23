from tkinter import *
#from main import next_card
import tkinter as tk
import subprocess
import csv
from Flashcard import Flashcard

BACKGROUND_COLOR = "#050D54"

k=1
m=k+2
def create_new_window(root):
    window = Toplevel(root)
    window.title("Flashcard app")
    window.config(background=BACKGROUND_COLOR)
    return window
    
def add_frames_from_csv(root):
    
    with open("flashcards.csv") as f:
        reader = csv.reader(f)
        i=1
        global k
        #self.tk
        for row in reader:
            if len(row)>0:
              verso=row[0]
              recto=row[1]
              label=row[2]
              color=row[3]
              data_file = row[4]
              history_file = row[5]
              info_frame =tk.Frame(root)
              info_frame.grid(row= k, column=i, padx=20, pady=20 )
              info_frame.config(bg='#050D54')
              
              fCard=Flashcard(label,recto,verso,color,data_file,history_file)
              print(fCard)

              button=Button(info_frame, text=row[2], font=("Courrier", 25),cursor='hand2', height=4, width=19, bg=row[3], fg='white', command=lambda: [fCard.show_window(create_new_window(root))])
              button.grid(row=0, column=0, pady=0,  padx=2, columnspan=10, sticky="ne")
              button11=Button(info_frame,image=image_ajout1,borderwidth=0,highlightthickness=0, cursor='hand2', command=fCard.ajouter_carte)
              button11.grid(pady=4, padx=1, row=2, column=3,sticky="w")
              button12=Button(info_frame,image=image_ajout2,borderwidth=0,highlightthickness=0, cursor='hand2', command=fCard.modifier_carte)
              button12.grid(pady=1, padx=1, row=2, column=4, sticky="w")
              button13=Button(info_frame,image=image_ajout3,borderwidth=0,highlightthickness=0, cursor='hand2', command=fCard.dashboard)
              button13.grid(pady=1, padx=1, row=2, column=5, sticky="w")
              button14=Button(info_frame,image=image_ajout4,borderwidth=0,highlightthickness=0, cursor='hand2', command=fCard.playHangMan)
              button14.grid(pady=1, padx=1, row=2, column=6, sticky="w")
              button15=Button(info_frame,image=image_ajout5,borderwidth=0,highlightthickness=0, cursor='hand2', command=fCard.supprimer_carte)
              button15.grid(pady=1, padx=1, row=2, column=7, sticky="w")
              i+=1
              if i%3==0:
                i=0
                k+=1


def run_game_script():
    subprocess.call(["python", "hangman.py"])

def add_button():
    subprocess.call(["python", "ajoutCategorie.py"])


root=Tk()
root.title('SmartReview')
root.config(background='#050D54')
# Set window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to full screen
root.geometry("%dx%d+0+0" % (screen_width, screen_height))

# create a canvas widget
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.config(bg='#050D54')
# create a scrollbar widget
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# create a frame inside the canvas to hold the grid elements
frame1 = tk.Frame(canvas)
frame1.config(bg='#050D54')
frame1.grid(padx=0,pady=0)
canvas.create_window((0, 0), window=frame1, anchor=tk.NW)


# add grid elements to the frame
image_ajt=PhotoImage(file="images/logo.png")
label1= Label(frame1, image=image_ajt, borderwidth=0)
label1.grid(padx=0,row=0,columnspan=6, sticky="w", column=0)
#image_ajt2=PhotoImage(file="images/smartReview.png")
#label1= Label(root, image=image_ajt2, borderwidth=0)
#label1.grid(padx=0,pady=18,row=0,sticky="ne", column=1 )#050D54
#label1= Label(root, text="FlashCards",font=("courrier", 40, 'bold'), bg='', fg='#38ADFC')
#label1.grid(padx=0,pady=18,row=0, column=0, sticky="ne")

#principalFrame
frame = tk.Frame(frame1)
frame.config(bg='#050D54')
frame.grid(row=1, column=0,padx=20,pady=0)

button=Button(frame, text='frToEng', font=("Courrier", 25),bg='#FAD727' , fg='white', height=4, width=19)
button.grid(row=1, column=0, pady=0, padx=2, columnspan=10, sticky="ne")

image_ajout1=PhotoImage(file="images/addCard.png")
image_ajout2=PhotoImage(file="images/edit.png")
image_ajout3=PhotoImage(file="images/graph.png")
image_ajout4=PhotoImage(file="images/game.png")
image_ajout5=PhotoImage(file="images/trash.png")

button6=Button(frame,image=image_ajout1,borderwidth=0,highlightthickness=0, cursor='hand2')
button6.grid(pady=5, padx=0, row=2, column=3,sticky="w")
button7=Button(frame,image=image_ajout2,borderwidth=0,highlightthickness=0, cursor='hand2')
button7.grid(pady=1, padx=0, row=2, column=4, sticky="w")
button8=Button(frame,image=image_ajout3,borderwidth=0,highlightthickness=0, cursor='hand2')
button8.grid(pady=1, padx=0, row=2, column=5, sticky="w")
button9=Button(frame,image=image_ajout4,borderwidth=0,highlightthickness=0, cursor='hand2')
button9.grid(pady=1, padx=0, row=2, column=6, sticky="w")
#button10=Button(frame,image=image_ajout5,borderwidth=0, highlightthickness=0,  relief="flat", cursor='hand2')
#button10.grid(pady=1, padx=0, row=2, column=7, sticky="w")

add_frames_from_csv(frame1)

image_ajout=PhotoImage(file="images/add.png")
#image_ajout = image_ajout.subsample(2, 2)relief="raised", bd=0 
button =Button(frame1,image=image_ajout,width=60,bg='white',height=60, borderwidth=0, cursor='hand2', border='0', command=add_button)
button.config()
button.grid(pady=0, padx=10, row=3, column=2)
#output_button = Button(root, text="Return Output", command=return_output)
#output_button.grid(row=2, column=0)



# configure the canvas to resize when the window size changes
def on_canvas_resize(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", on_canvas_resize)

root.mainloop()