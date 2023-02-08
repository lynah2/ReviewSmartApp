from tkinter import *
import pandas 
import random

window = Tk()
BACKGROUND_COLOR="#B1DDC6"
#--------------------------------------
def pick_card():
    global new_card,timer
    window.after_cancel(timer)
    new_card=random.choice(learn_words)
    french=new_card["French"]
    canvas.itemconfig(font_side,image=font_image)
    canvas.itemconfig(title, text="French")
    canvas.itemconfig(word,text=french)
    window.config(bg=BACKGROUND_COLOR)
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    timer=window.after(3000,flip_card)
def flip_card():
    english=new_card["English"]
    canvas.itemconfig(front_side,image=back_image)
    canvas.config(bg="white", highlightthickness=0)
    canvas.itemconfig(title, text="English")
    canvas.itemconfig(word,text=english)
    window.config(bg="white")
def is_known():
    learn_word.remove(new_card)
    data=pandas.DataFrame(learn_words)
    data.to_csv("knownWords.csv")
    pick_card()
#----------------------------------
window.title("Flash card")
window.config(padx=50,pady=50, bg=BACKGROUND_COLOR)
canvas=Canvas(width=800,height=526)

font_image=PhotoImage(file="front.png")
back_image=PhotoImage(file="back.png")
cross_image=PhotoImage(file="wrong.png")
correct_image=PhotoImage(file="correct.png")

front_side=canvas.create_image(400,263,image=font_image)
title=canvas.create_text(400,200,text="",font=("Arial",20))
word=canvas.create_text(400,263,text="",font=("Arial",20,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

correct_Button=Button(image=correct_image,highlightthickness=0,command=is_known)
correct_Button.grid(row=1,column=1)
correct_Button=Button(image=cross_image,highlightthickness=0,command=pick_card)
correct_Button.grid(row=1,column=0)

timer=window.after(3000,flip_card)
try:
    data=pandas.read_csv("frToEng.csv")
except:
    data=pandas.read_csv("frToEng.csv")
learn_words=data.to_dict(orient="records")


pick_card()
window.mainloop()
