import random
from tkinter import *
from tkinter import messagebox
import csv

def hangman(data_file):
    score = 0
    run = True

    # main loop
    while run:
        root = Tk()
        root.geometry('905x600')
        root.title('HANG MAN')
        root.config(bg = '#E7FFFF')
        count = 0
        win_count = 0

        # choosing word
        with open(data_file) as f:
            l= csv.reader(f)
            rows = list(l)
            random_row = random.choice(rows)
            selected_word=random_row[1]
            toGuess=random_row[0]
        
        
        # creation of word dashes variables
        x = 250
        for i in range(0,len(selected_word)):
            x += 60
            exec('d{}=Label(root,text="_",bg="#E7FFFF",font=("arial",20))'.format(i))
            exec('d{}.place(x={},y={})'.format(i,x,350))
            
        #letters icon
        al = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for let in al:
            exec('{}=PhotoImage(file="images/{}.png")'.format(let,let))
            
        # hangman images
        h123 = ['h1','h2','h3','h4','h5','h6','h7']
        for hangman in h123:
            exec('{}=PhotoImage(file="images/{}.png")'.format(hangman,hangman))
            
        #letters placement
        button = [['b1','a',0,470],['b2','b',70,470],['b3','c',140,470],['b4','d',210,470],['b5','e',280,470],['b6','f',350,470],['b7','g',420,470],['b8','h',490,470],['b9','i',560,470],['b10','j',630,470],['b11','k',700,470],['b12','l',770,470],['b13','m',840,470],['b14','n',0,530],['b15','o',70,530],['b16','p',140,530],['b17','q',210,530],['b18','r',280,530],['b19','s',350,530],['b20','t',420,530],['b21','u',490,530],['b22','v',560,530],['b23','w',630,530],['b24','x',700,530],['b25','y',770,530],['b26','z',840,530]]

        for q1 in button:
            exec('{}=Button(root,bd=0,command=lambda:check("{}","{}"),bg="#E7FFFF",activebackground="#E7FFFF",font=10,image={})'.format(q1[0],q1[1],q1[0],q1[1]))
            exec('{}.place(x={},y={})'.format(q1[0],q1[2],q1[3]))
            
        #hangman placement
        han = [['c1','h1'],['c2','h2'],['c3','h3'],['c4','h4'],['c5','h5'],['c6','h6'],['c7','h7']]
        for p1 in han:
            exec('{}=Label(root,bg="#E7FFFF",image={})'.format(p1[0],p1[1]))

        # placement of first hangman image
        c1.place(x = 300,y =- 50)
        
        #exit button
        def close():
            global run
            answer = messagebox.askyesno('ALERT','YOU WANT TO EXIT THE GAME?')
            if answer == True:
                run = False
                root.destroy()
                
        e1 = PhotoImage(file = 'images/exit.png')
        ex = Button(root,bd = 0,command = close,bg="#E7FFFF",activebackground = "#E7FFFF",font = 10,image = e1)
        ex.place(x=770,y=10)
        s2 = 'SCORE:'+str(score)
        s1 = Label(root,text = s2,bg = "#E7FFFF",font = ("arial",25))
        s1.place(x = 10,y = 10)
        tentatives=str(6-count)
        s3 = Label(root,text='-----------------------------\n Vous avez '+tentatives+' tentatives\n pour trouver l\'équivalent  \n du mot suivant: \n"'+toGuess+'"\n-----------------------------',
                bg = "black",
                fg="white",
                font = ("arial",15))
        s3.place(x = 10,y = 100)
        # button press check function
        def check(letter,button):
            global count,win_count,run,score
            exec('{}.destroy()'.format(button))
            if letter in selected_word:
                for i in range(0,len(selected_word)):
                    if selected_word[i] == letter:
                        win_count += 1
                        exec('d{}.config(text="{}")'.format(i,letter.upper()))
                if win_count == len(selected_word):
                    score += 1
                    answer = messagebox.askyesno('GAME OVER','YOU WON!\nWANT TO PLAY AGAIN?')
                    if answer == True:
                        run = True
                        root.destroy()   
                    else:
                        run = False
                        root.destroy()
            else:
                count += 1
                exec('c{}.destroy()'.format(count))
                exec('c{}.place(x={},y={})'.format(count+1,300,-50))
                if count == 6:
                    answer = messagebox.askyesno('GAME OVER','YOU LOST!\nWANT TO PLAY AGAIN?')
                    if answer == True:
                        run = True
                        score = 0
                        root.destroy()
                    else:
                        run = False
                        root.destroy()         
        root.mainloop()

