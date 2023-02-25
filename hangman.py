from tkinter import *
import random
import tkinter.messagebox as msg
import csv

class HangMan:
    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name
        self.root = Tk()  # INSTANCE OF Tk()
        self.width, self.height = 500, 600  # HEIGHT AND WIDTH OF THE CREATED WINDOW
        # // means to divide the value and don't give the decimal value and called (FLOOR DIVISION)
        self.s_width = ((self.root.winfo_screenwidth() // 2) - (self.width // 2))  # (WIDTH OF THE MONITOR DISPLAY)//2 - (WIDTH OF THE CREATED WINDOW)//2
        self.s_height = ((self.root.winfo_screenheight() // 2) - (self.height // 2))   # (HEIGHT OF THE MONITOR DISPLAY)//2 - (HEIGHT OF THE CREATED WINDOW)//2
        self.root.geometry(f'{self.width}x{self.height}+{self.s_width}+{self.s_height}')  # AFTER THE MONITOR DISPLAY HEIGHT AND WIDTH THE HEIGHT AND WIDTH OF THE CREATED WINDOW SHOULD COME TO CENTER IT
        self.root.title("Hang-Man Game")  # TITLE OF THE WINDOW
        self.root.resizable(0, 0)  # WINDOW CAN'T BE RESIZED
        self.root.configure(bg='#050D54')
  
        #image_ajt=PhotoImage(file="images/hangman.png")
        #label1= Label(self.root, image=image_ajt, borderwidth=0)
        #label1.pack()


        # CREATING THE FIGURE OF HANG MAN #
        self.canvas = Canvas(self.root, width=500, height=260)  # CREATING A CANVAS ON WHICH WE CAN DRAW LINES AND SHAPES
        self.canvas.pack(pady=30)# PACKING THE CANVAS TO BE DISPLAYED ON WINDOW
        self.canvas.configure(bg='#050D54')
        
        label = Label(self.canvas, text="HANGMAN",font=("Candara", 30, "bold"), fg='red', bg="#050D54")
        self.canvas.create_window(0, 0, anchor="nw", window=label)

        '''
        img =PhotoImage(file="images/hangman.png")
        self.canvas.create_image(0, 0, anchor="nw", image=img)
        '''

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
        
        #self.scramble(self.picked_word)
        self.count = 1
        self.picked_word,self.toGuess = self.choose()
        self.value = StringVar()
        self.show = "Donnez l'équivalent de "+self.equivalent
        self.correct = NONE

        self.lbl = Label(self.root, text=self.show, font=("Candara", 25, "bold"),bg='#050D54',fg='#38ADFC')  # MAKING THE LABEL WHICH WILL SHOW YOU THE JUMBLE WORDS
        self.lbl.pack()  # PACKING THE LABEL

        self.txt = Entry(self.root,  font=("Candara", 25, "bold"), justify=CENTER, relief=GROOVE, bd=2)  # IN THIS THE USER WILL ANSWER
        self.txt.pack(pady=10)  # PACKING THE ENTRY WIDGETtextvariable=self.value,
        self.value=''

        self.btn = Button(self.root, text="SUBMIT", font=("Candara", 20, "bold"), relief=GROOVE, bg="red",fg='white', command=self.get_entry_value)
        #self.btn = Button(self.root, text="SUBMIT", font=("Candara", 20, "bold"), relief=GROOVE, bg="orange",fg='white', command=self.process)  # CLICKED IT value WHETHER THE ANSWER WAS RIGHT ON WRONG
        self.btn.pack(pady=20)  # PACKING THE BUTTON
        #self.root.bind('<Return>', self.process)  # BINDING ENTER KEY TO VALIDATE
        #self.root.bind('<Return>', lambda event: (self.process(), self.validate()))

        self.root.mainloop()

    def choose(self):
        with open(self.csv_file_name) as f:
            l= csv.reader(f)
            rows = list(l)
            random_row = random.choice(rows)
            #global self.equivalent
            self.equivalent=random_row[0]
            self.toGuess=random_row[1]
            pick = self.toGuess
            return (pick,self.equivalent)
    
    def get_entry_value(self):
        self.value = self.txt
        print("Entry value:", self.value)
        self.process()
        

    def scramble(self, word):
        print(word)
        random_word = random.sample(word, len(word))  # IT MAKE A STRING INTO A LIST BY BRAKING EACH LETTER
        scrambled = ''.join(random_word)
        return scrambled
    
    def validate(self):
        #k=self.value
        #print(k)
        print(self.picked_word)
        #global count, picked_word, c1, c2, c3, c4, c5, show
        if self.value.get().upper() == self.picked_word.upper():
            self.picked_word,self.equivalent = self.choose()
            self.show = "Donnez l'équivalent de "+self.equivalent
            self.txt.delete(0, END)
            self.lbl.config(text=self.show)
        else:
            if self.count == 1 and self.value.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c1)
                self.txt.delete(0, END)
            elif self.count == 2 and self.value.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c2)
                self.txt.delete(0, END)
            elif self.count == 3 and self.value.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c3)
                self.txt.delete(0, END)
            elif self.count == 4 and self.value.get().upper() != self.picked_word:
                self.count += 1
                self.canvas.delete(self.c4)
                self.txt.delete(0, END)
            elif self.count == 5 and self.value.get().upper() != self.picked_word:
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
            


    # PROCESSING TO VALIDATE #
    def process(self, event=""):
        #global correct
        #self.correct = TRUE
        #self.validate()
        
        if self.value.get().isalpha():
            self.correct = TRUE
            self.validate()
        else:
            self.correct = FALSE
            msg.showerror('Error', 'Please make use of only Alphabets')
        


#test
#csvFile='frToEng.csv'
#hangmantest=HangMan(csvFile)