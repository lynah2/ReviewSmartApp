import pandas as pd
import re
import csv
from datetime import datetime
BACKGROUND_COLOR = "#050D54"
import random
from tkinter import *

to_learn = {}
current_card = {}
learned = {}

try: # try running this line of codeC:\Users\Lenovo\Desktop\ankiProject\
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
    data_comprehensible = data[data.apply(lambda x: is_comprehensible(x['French'], x['English']), axis=1)]
    data_comprehensible.to_csv("frToEng_comprehensible.csv", index=False)
    to_learn = data.to_dict(orient="records")

#------------------------ Generating a English word ----------

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # English_word = random_pair['English']
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text = "French", fill = "white")
    canvas.itemconfig(card_word, text=current_card["French"], fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data_k = pd.DataFrame(to_learn)
    data_k.to_csv("frToEng_known.csv", index=False)
    learned.update(current_card)
    dataLearned=list(learned.values())
    wordLearnedDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keys = ['French', 'English', 'learningDate']
    dataLearned.append(wordLearnedDate)
    d = {keys[i]: dataLearned[i] for i in range(len(keys))}
    #learned_words= pd.DataFrame(d)
    #learned_words.to_csv("learned_words.csv", index=False) 
    with open("learn_words2.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(dataLearned) 
    # index = false discrads the index numbers
    next_card()
#------------------------ FlashCard UI Setup -------------------------------

window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card) # 3000 milliseocnds = 3 seconds

canvas = Canvas(width=800, height=326)
card_front_img=PhotoImage(file="front.gif")
card_back_img =PhotoImage(file="back.gif")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
# Positions are related to canvas so 400 will be halfway in width
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"), tags="word")
# canvas should go in the middle
canvas.grid(row=0, column=0, columnspan=2)

cross_image=PhotoImage(file="wrong.gif")
cross_image = cross_image.subsample(2, 2)
unknown_button = Button(image=cross_image, command = next_card)
unknown_button.grid(row=1, column=0, sticky="W")

check_image=PhotoImage(file="correct.gif")
check_image = check_image.subsample(2, 2)
known_button = Button(image=check_image, command=is_known)
known_button.grid(row=1, column=1, sticky="E")

next_card()
window.mainloop()