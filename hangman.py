from tkinter import *
import random
import tkinter.messagebox as msg
import csv

class HangMan:
    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name
        self.root = Tk()  # INSTANCE OF Tk()
        self.width, self.height = 500, 550  # HEIGHT AND WIDTH OF THE CREATED WINDOW
        # // means to divide the value and don't give the decimal value and called (FLOOR DIVISION)
        self.s_width = ((self.root.winfo_screenwidth() // 2) - (self.width // 2))  # (WIDTH OF THE MONITOR DISPLAY)//2 - (WIDTH OF THE CREATED WINDOW)//2
        self.s_height = ((self.root.winfo_screenheight() // 2) - (self.height // 2))   # (HEIGHT OF THE MONITOR DISPLAY)//2 - (HEIGHT OF THE CREATED WINDOW)//2
        self.root.geometry(f'{self.width}x{self.height}+{self.s_width}+{self.s_height}')  # AFTER THE MONITOR DISPLAY HEIGHT AND WIDTH THE HEIGHT AND WIDTH OF THE CREATED WINDOW SHOULD COME TO CENTER IT
        self.root.title("Hang-Man Game")  # TITLE OF THE WINDOW
        self.root.resizable(0, 0)  # WINDOW CAN'T BE RESIZED
        self.root.configure(bg='#050D54')
        # CREATING THE FIGURE OF HANG MAN #
        self.canvas = Canvas(self.root, width=500, height=260)  # CREATING A CANVAS ON WHICH WE CAN DRAW LINES AND SHAPES
        self.canvas.pack(pady=30)# PACKING THE CANVAS TO BE DISPLAYED ON WINDOW
        self.canvas.configure(bg='#050D54')
        self.canvas.create_line(150, 260, 250, 260, width=3, fill='white')  # BASE LINE OF THE STAND
        self.canvas.create_line(200, 260, 200, 40, width=3, fill='white')  # LINE OF THE STAND
        self.canvas.create_line(200, 90, 250, 40, width=3, fill='white')  # SUPPORTER OF STAND
        self.canvas.create_line(200, 40, 300, 40, width=3, fill='white')  # TOP LINE OF STAND
        self.canvas.create_line(300, 40, 300, 70, width=3, fill='white')  # ROPE OF THE STAND
        self.canvas.create_oval(280, 70, 320, 100, width=3, fill='white')  # HEAD OF THE MAN
        self.c5 = self.canvas.create_line(300, 100, 300, 180, width=3, fill='white')  # STOMACH OF THE MAN :)
        self.c4 = self.canvas.create_line(300, 105, 270, 155, width=3, fill='white')  # LEFT HAND OF THE MAN
        self.c3 = self.canvas.create_line(300, 105, 330, 155, width=3, fill='white')  # RIGHT HAND OF THE MAN
        self.c2 = self.canvas.create_line(300, 180, 270, 230, width=3, fill='white')  # LEFT LEG OF THE MAN
        self.c1 = self.canvas.create_line(300, 180, 330, 230, width=3, fill='white')  # RIGHT LEG OF THE MAN
        
        self.count = 1
        self.picked_word = self.choose()
        self.check = StringVar()
        self.show = self.scramble(self.picked_word)
        self.correct = NONE

        self.lbl = Label(self.root, text=self.show, font=("Candara", 25, "bold"),bg='#050D54',fg='#38ADFC')  # MAKING THE LABEL WHICH WILL SHOW YOU THE JUMBLE WORDS
        self.lbl.pack()  # PACKING THE LABEL

        self.txt = Entry(self.root, textvariable=self.check, font=("Candara", 25, "bold"), justify=CENTER, relief=GROOVE, bd=2)  # IN THIS THE USER WILL ANSWER
        self.txt.pack(pady=10)  # PACKING THE ENTRY WIDGET

        self.btn = Button(self.root, text="SUBMIT", font=("Candara", 20, "bold"), relief=GROOVE, bg="orange",fg='white', command=self.process)  # CLICKED IT CHECK WHETHER THE ANSWER WAS RIGHT ON WRONG
        self.btn.pack(pady=20)  # PACKING THE BUTTON
        self.root.bind('<Return>', self.process)  # BINDING ENTER KEY TO VALIDATE

        self.root.mainloop()

    def choose(self):
        with open(self.csv_file_name) as f:
            l= csv.reader(f)
            rows = list(l)
            random_row = random.choice(rows)
            selected_word=random_row[1]
            toGuess=random_row[0]
            pick = toGuess
            return pick

    def scramble(self, word):
        print(word)
        random_word = random.sample(word, len(word))  # IT MAKE A STRING INTO A LIST BY BRAKING EACH LETTER
        scrambled = ''.join(random_word)
        return scrambled
    
    def validate(self):
        #global count, picked_word, c1, c2, c3, c4, c5, show
        if self.check.get().upper() == self.picked_word.upper():
            self.picked_word = self.choose()
            self.show = self.scramble(self.picked_word)
            self.check.set("")
            self.lbl.config(text=self.show)
        else:
            if self.count == 1 and self.check.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c1)
            elif self.count == 2 and self.check.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c2)
            elif self.count == 3 and self.check.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c3)
            elif self.count == 4 and self.check.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c4)
            elif self.count == 5 and self.check.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c5)
                msg.showwarning("Game Over", "Please Try Again...")
                self.c1 = self.canvas.create_line(300, 180, 330, 230, width=3)
                self.c2 = self.canvas.create_line(300, 180, 270, 230, width=3)
                self.c3 = self.canvas.create_line(300, 105, 330, 155, width=3)
                self.c4 = self.canvas.create_line(300, 105, 270, 155, width=3)
                self.c5 = self.canvas.create_line(300, 100, 300, 180, width=3)
            if self.count == 6:
                self.count = 1
            self.check.set("")


    # PROCESSING TO VALIDATE #
    def process(self, event=""):
        self.correct = TRUE
        self.validate()
        #global correct
        # if self.check.get().isalpha():
        #     self.correct = TRUE
        #     self.validate()
        # else:
        #     self.correct = FALSE
        #     msg.showerror('Error', 'Please make use of only Alphabets')



#test
#csvFile='frToEng.csv'
#hangmantest=HangMan(csvFile)