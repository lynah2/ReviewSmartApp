import pandas as pd
import re
import datetime
from supermemo2 import SMTwo


BACKGROUND_COLOR = "#B1DDC6"
import random
from tkinter import *

to_learn = {}
current_card = {}

try: # try running this line of code
    data = pd.read_csv("frToEng.csv")
except FileNotFoundError:
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

if 'lastRevised' not in data.columns:   #updated in next_card
    data['lastRevised'] = 0

if 'repetition' not in data.columns:   #updated in next_card
    data['repetition'] = 0
data['repetition'] = data['repetition'].astype(int)

if 'correct' not in data.columns:   #updated if known
    data['correct'] = 0
data['correct'] = data['correct'].astype(int)

now = datetime.datetime.now().strftime("%Y-%m-%d")

if 'nextTime' not in data.columns:   #updated in next_card assuming user got it wrong then update in is_known if known
    data['nextTime'] = now 

if 'responseQuality' not in data.columns:   #updated in next_card assuming user got it wrong then update in is_known if known
    data['responseQuality'] = 0
data['responseQuality'] = data['responseQuality'].astype(int)


        
to_learn = data.to_dict(orient="records")
now = datetime.datetime.now().strftime("%Y-%m-%d")

print(len(to_learn))


Today = [d for d in to_learn if d['nextTime'] == now]
print(len(Today))

to_learn = [x for x in to_learn if x not in Today]
print(len(to_learn))

#print(Today)
i = 0

#------------------------ Generating a English word ----------

def next_card():
    global current_card, flip_timer
    global i
    window.after_cancel(flip_timer)
    i += 1

    print(i)
    
    if Today:
        current_card = random.choice(Today)
        Today.remove(current_card)
    elif to_learn:
        current_card = random.choice(to_learn)
        to_learn.remove(current_card)

    # Update the relevant row
    data.loc[data['English'] == current_card['English'], 'lastRevised'] = datetime.datetime.now().strftime("%Y-%m-%d")
    data.loc[data['English'] == current_card['English'], 'repetition'] += 1  
    
    data.loc[data['English'] == current_card['English'], 'responseQuality'] = calculate_responseQuality(current_card['correct'], current_card['repetition'])
    
    if current_card['repetition'] == 0: 
        data.loc[data['English'] == current_card['English'], 'nextTime'] = review = SMTwo.first_review(0,now).review_date
    else:
        data.loc[data['English'] == current_card['English'], 'nextTime'] = SMTwo(review.easiness, review.interval, review.repetitions).review(current_card['responseQuality'], now).review_date
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
    
    # Load the CSV file into a DataFrame
    data = pd.read_csv("frToEng.csv")
    # Update the relevant row
    data.loc[data['English'] == current_card['English'], 'correct'] += 1
    data.loc[data['English'] == current_card['English'], 'responseQuality'] = calculate_responseQuality(current_card['correct'], current_card['repetition'])

    if current_card['repetition'] == 0: 
        data.loc[data['English'] == current_card['English'], 'nextTime'] = review = SMTwo.first_review(0,now).review_date
    else:
        data.loc[data['English'] == current_card['English'], 'nextTime'] = SMTwo(review.easiness, review.interval, review.repetitions).review(current_card['responseQuality'], now).review_date

    data.to_csv("frToEng.csv", index=False)
    # index = false discrads the index numbers
    next_card()
    
def calculate_responseQuality(correct, repetition):
    if repetition != 0:
        res = correct / repetition
    else:
        res = 0
    if res == 1:
        return 5
    elif res > 0.75:
        return 4
    elif res > 0.5:
        return 3
    elif res > 0.25:
        return 2
    elif res == 0:
        return 0
    else:   
        return 1 






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