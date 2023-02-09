import pandas as pd
import re
import datetime

BACKGROUND_COLOR = "#B1DDC6"
import random
from tkinter import *

to_learn = {}
current_card = {}

try: # try running this line of code
    data = pd.read_csv("frToEng.csv")
except FileNotFoundError:
    # If for the first time we are running it
    # the .csv file might not be present
    # and FileNotFoundError might pop up
    data = pd.read_csv("frToEng.csv") 
else:
    data = pd.read_csv("frToEng.csv")
    # Define a function to check if a word is comprehensible
def is_comprehensible(word_f, word_e):
    if not re.match("^[a-zA-Z]+$", word_f) or not re.match("^[a-zA-Z]+$", word_e) or word_f.lower() == word_e.lower():
        return False
    return True

# Filter out the words that are not comprehensible
data = data[data.apply(lambda x: is_comprehensible(x['French'], x['English']), axis=1)]
data.to_csv("frToEng.csv", index=False)

if 'lastRevised' not in data.columns:
    data['lastRevised'] = 0
if 'learned' not in data.columns:
    data['learned'] = 'n'
if 'nextTime' not in data.columns:
    data['nextTime'] = 0
to_learn = data.to_dict(orient="records")
now = datetime.datetime.now().strftime("%Y-%m-%d")

Today = [d for d in to_learn if d['nextTime'] == now]

print(Today)


#------------------------ Generating a English word ----------

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    
    if Today:
        current_card = random.choice(Today)
    elif to_learn:
        current_card = random.choice(to_learn)

    # Update the relevant row
    data.loc[data['French'] == current_card['French'], 'last_revised'] = datetime.datetime.now().strftime("%Y-%m-%d")
    data.loc[data['French'] == current_card['French'], 'learned'] = 'n'
    
    data.loc[data['French'] == current_card['French'], 'nextTime'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # Write the DataFrame back to the file
    data.to_csv("frToEng.csv", index=False)

    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text = "French", fill = "white")
    canvas.itemconfig(card_word, text=current_card["French"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    if current_card in Today:
        Today.remove(current_card)
    elif current_card in to_learn:
        to_learn.remove(current_card)
    # Load the CSV file into a DataFrame
    data = pd.read_csv("frToEng.csv")
    # Update the relevant row
    data.loc[data['French'] == current_card['French'], 'learned'] = 'y'
    data.loc[data['French'] == current_card['French'], 'nextTime'] = (datetime.datetime.now() + datetime.timedelta(days=7))

    data.to_csv("frToEng.csv", index=False)
    # index = false discrads the index numbers
    next_card()
    



#------------------------ FlashCard UI Setup -------------------------------

window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card) # 3000 milliseocnds = 3 seconds

canvas = Canvas(width=800, height=326)
card_front_img = PhotoImage(file="images/white.png")
card_back_img = PhotoImage(file="images/black.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
# Positions are related to canvas so 400 will be halfway in width
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"), tags="word")
# canvas should go in the middle
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, command = next_card)
unknown_button.grid(row=1, column=0, sticky="W")

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.grid(row=1, column=1, sticky="E")

next_card()
window.mainloop()