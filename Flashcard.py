import pandas as pd
import re
import datetime
from main import is_comprehensible
from supermemo2 import SMTwo
import random
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

class Flashcard:
    @staticmethod
    def is_comprehensible(word_f, word_e):
        if not re.match("^[a-zA-Z]+$", word_f) or not re.match("^[a-zA-Z]+$", word_e) or word_f.lower() == word_e.lower():
            return False
        return True
        
    def __init__(self, data_file, window):
        self.data = pd.read_csv(data_file)
        self.to_learn = {}
        self.self.current_card = {}
        self.i = 0
        
        # Filter out the words that are not comprehensible
        self.data = self.data[self.data.apply(lambda x: is_comprehensible(x['French'], x['English']), axis=1)]
        self.data.to_csv("frToEng.csv", index=False)
        
        
        if 'lastRevised' not in self.data.columns:   #updated in next_card
            self.data['lastRevised'] = 0

        if 'repetition' not in self.data.columns:   #updated in next_card
            self.data['repetition'] = 0
        self.data['repetition'] = self.data['repetition'].astype(int)

        if 'correct' not in self.data.columns:   #updated if known
            self.data['correct'] = 0
        self.data['correct'] = self.data['correct'].astype(int)

        now = datetime.datetime.now().strftime("%Y-%m-%d")

        if 'nextTime' not in self.data.columns:   #updated in next_card assuming user got it wrong then update in is_known if known
            self.data['nextTime'] = now 


        if 'interval' not in self.data.columns:   #updated by review
            self.data['inteval'] = 1

        if 'repetitions_rev' not in self.data.columns:   #updated by review
            self.data['repetitions_rev'] = 0

        if 'responseQuality' not in self.data.columns:   #updated in next_card assuming user got it wrong then update in is_known if known
            self.data['responseQuality'] = 0
        self.data['responseQuality'] = self.data['responseQuality'].astype(int)

                
        self.to_learn = self.data.to_dict(orient="records")
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        print(len(self.to_learn))
        self.Today = [d for d in self.to_learn if d['nextTime'] == now]
        print(len(self.Today))

        self.to_learn = [x for x in self.to_learn if x not in self.Today]
        print(len(self.to_learn))

        #------------------------ FlashCard UI Setup -------------------------------
        self.window = window 
        self.canvas = Canvas(width=800, height=326)
        self.card_front_img = PhotoImage(file="images/white.png")
        self.card_back_img = PhotoImage(file="images/Black.png")
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.card_title = self.canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.right_img = PhotoImage(file="images/right.png")
        self.right_button = Button(image=self.right_img, highlightthickness=0, command=self.is_known)
        self.right_button.grid(row=1, column=0)

        self.wrong_img = PhotoImage(file="images/wrong.png")
        self.wrong_button = Button(image=self.wrong_img, highlightthickness=0, command=self.next_card)
        self.wrong_button.grid(row=1, column=1)

        self.flip_timer = self.window.after(3000, func=self.flip_card)

        

    def flip_card(self):
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
        self.canvas.itemconfig(self.card_word, text=self.self.current_card["English"], fill="white")
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)

    def next_card(self):
        self.window.after_cancel(self.flip_timer)

        if self.to_learn:
            self.self.current_card = random.choice(self.to_learn)
            self.to_learn.remove(self.self.current_card)
        else:
            self.to_learn = self.data.to_dict(orient="records")
            self.self.current_card = random.choice(self.to_learn)

        # Update the relevant row
            self.data.loc[self.data['English'] == self.self.current_card['English'], 'lastRevised'] = datetime.datetime.now().strftime("%Y-%m-%d")
            self.data.loc[self.data['English'] == self.self.current_card['English'], 'repetition'] += 1  
            
            self.data.loc[self.data['English'] == self.self.current_card['English'], 'responseQuality'] = calculate_responseQuality(self.current_card['correct'], self.current_card['repetition'])
            
            if self.self.current_card['repetition'] == 0:
                review = SMTwo.first_review(0,now)

                self.data.loc[self.data['English'] == self.current_card['English'], 'nextTime'] = review.review_date
                self.data.loc[self.data['English'] == self.current_card['English'], 'interval'] = review.interval
                self.data.loc[self.data['English'] == self.current_card['English'], 'easiness'] = review.easiness
                self.data.loc[self.data['English'] == self.current_card['English'], 'repetitions_rev'] = review.repetitions
            else:
                easiness = float(self.current_card['easiness'])
                interval = int(self.current_card['interval'])
                repetitions = int(self.current_card['repetitions_rev'])
                review = SMTwo(easiness, interval, repetitions)
                
                self.data.loc[self.data['English'] == self.current_card['English'], 'nextTime'] = review.review(self.current_card['responseQuality'], self.current_card['nextTime']).review_date
                self.data.loc[self.data['English'] == self.current_card['English'], 'interval'] = review.interval
                self.data.loc[self.data['English'] == self.current_card['English'], 'easiness'] = review.easiness
                self.data.loc[self.data['English'] == self.current_card['English'], 'repetitions_rev'] = review.repetitions
            # Write the DataFrame back to the file
            self.data.to_csv("frToEng.csv", index=False)

        self.canvas.itemconfig(self.card_title, text="French", fill="black")
        self.canvas.itemconfig(self.card_word, text=self.self.current_card["French"], fill="black")
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.flip_timer = self.window.after(5000, func=self.flip_card)
    

    def is_known(self):
        self.to_learn.remove(self.self.current_card)
        self.data.loc[self.data['English'] == self.self.current_card['English'], 'correct'] += 1
        self.data.to_csv(self.data_file, index=False)
        self.next_card()

    

mafenetre = Tk()
mafenetre.title("Anki")
mafenetre.config(background=BACKGROUND_COLOR)

# create instance d'objet Flashcard
flashcard = Flashcard('frToEng.csv', mafenetre)

