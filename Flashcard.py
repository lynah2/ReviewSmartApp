from tkinter import messagebox
import pandas as pd
import re
import datetime
from supermemo2 import SMTwo
import random
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import Counter
import csv
import os
from Hangman import HangMan



BACKGROUND_COLOR = "#050D54"

class Flashcard:
    
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def is_comprehensible(word_f, word_e):
        if not re.match("^[a-zA-Z]+$", word_f) or not re.match("^[a-zA-Z]+$", word_e) or word_f.lower() == word_e.lower():
            return False
        return True
        
        
    def __init__(self,label, recto, verso, color,data_file,history):
        global now, i
        
        self.label = label
        self.recto = recto
        self.verso = verso
        self.color = color

        now = datetime.datetime.now().strftime("%Y-%m-%d")

        self.data_file = data_file
        self.data = pd.read_csv(data_file)

        self.history= history
        
        self.to_learn = {}
        self.current_card = {}
        self.i = 0
        
        # Filter out the words that are not comprehensible
        self.data = self.data[self.data.apply(lambda x: self.is_comprehensible(x[self.verso], x[self.recto]), axis=1)]
        self.data.to_csv(self.data_file, index=False)
        
        if 'correct' not in self.data.columns:   #updated if known
            self.data['correct'] = 0
        self.data['correct'] = self.data['correct'].fillna(0).astype(int)

        if 'repetition' not in self.data.columns:   #updated in next_card
            self.data['repetition'] = 0
        self.data['repetition'] = self.data['repetition'].fillna(0).astype(int)

        if 'lastRevised' not in self.data.columns:   #updated in next_card
            self.data['lastRevised'] = 0

        if 'nextTime' not in self.data.columns:   #updated in next_card assuming user got it wrong then update in is_known if known
            self.data['nextTime'] = now 

        if 'easiness' not in self.data.columns:   #updated by review
            self.data['easiness'] = 1

        if 'interval' not in self.data.columns:   #updated by review
            self.data['interval'] = 1

        if 'repetitions_rev' not in self.data.columns:   #updated by review
            self.data['repetitions_rev'] = 0

        if 'responseQuality' not in self.data.columns:   #updated in next_card assuming user got it wrong then update in is_known if known
            self.data['responseQuality'] = 0
        self.data['responseQuality'] = self.data['responseQuality'].fillna(0).astype(int)

        #Francais        
        self.cards = self.data.to_dict(orient="records")
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        print(len(self.to_learn))
        self.Today = [d for d in self.to_learn if d['nextTime'] == now]
        print(len(self.Today))

        self.to_learn = [x for x in self.cards if x not in self.Today]
        print(len(self.to_learn))
        
    def get_nb_cards(self):
        return len(self.data)

    def get_nb_passed(self):
        return len(self.data[self.data['responseQuality'] >= 3])

    def get_color(self):
        return self.color

    def flip_card(self):
        
        self.canvas.itemconfig(self.card_title, text=self.verso, fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card[self.verso], fill="white")
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)

    def next_card(self,window):

        window.after_cancel(self.flip_timer)
        if self.to_learn:
            self.current_card = random.choice(self.to_learn)
            self.to_learn.remove(self.current_card)
        else:
            self.to_learn = self.data.to_dict(orient="records")
            self.current_card = random.choice(self.to_learn)

        # Update the relevant row
        self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'lastRevised'] = datetime.datetime.now().strftime("%Y-%m-%d")
        self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'repetition'] += 1  
        
        response_quality = self.calculate_responseQuality(self.current_card['correct'], self.current_card['repetition']+1)
        self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'responseQuality'] = int(response_quality)
        
        if self.current_card['repetition'] == 0:
            review = SMTwo.first_review(0,now)

            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'nextTime'] = review.review_date
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'interval'] = review.interval
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'easiness'] = review.easiness
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'repetitions_rev'] = review.repetitions
        else:
            easiness = float(self.current_card['easiness'])
            interval = int(self.current_card['interval'])
            repetitions = int(self.current_card['repetitions_rev'])
            review = SMTwo(easiness, interval, repetitions).review(response_quality, self.current_card['nextTime'])
            
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'nextTime'] = review.review_date
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'interval'] = review.interval
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'easiness'] = review.easiness
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'repetitions_rev'] = review.repetitions
        
        # Write the DataFrame back to the file
        self.data.to_csv(self.data_file, index=False)

        self.canvas.itemconfig(self.card_title, text=self.recto, fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_card[self.recto], fill="black")
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.flip_timer = window.after(3000, func=self.flip_card)
    

    def get_window(self):
        return self.window

    def show_window(self,window):
        # self.window = tkinter.Tk()
        # self.window.title("Flashcard app")
        # self.window.config(background=BACKGROUND_COLOR)

        self.canvas = Canvas(window,width=800, height=326)
        
        self.card_front_img = PhotoImage(file="images/white.png")
        self.card_back_img = PhotoImage(file="images/Black.png")
        self.right_img = PhotoImage(file="images/right.png")
        self.wrong_img = PhotoImage(file="images/wrong.png")

        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.card_title = self.canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
        
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)
        
        self.right_button = Button(window,image=self.right_img, highlightthickness=0, command=lambda: (self.is_known(window)))
        self.right_button.grid(row=1, column=0,pady='10')
        self.wrong_button = Button(window,image=self.wrong_img, highlightthickness=0, command=lambda: (self.next_card(window)))
        self.wrong_button.grid(row=1, column=1, pady='10')

        # self.graph1 = Button(text="First graph", command=self.graph_correct)
        # self.graph1.grid(row=2, column=0, columnspan=5)

        # self.graph2 = Button(text="Second graph", command=self.graph_level)
        # self.graph2.grid(row=2, column=1, columnspan=5)

        # self.dash = Button(text="Dashboard", command=self.dashboard)
        # self.dash.grid(row=2, column=2, columnspan=5)

        # self.ajout = Button(text="Ajout", command=self.ajouter_carte)
        # self.ajout.grid(row=3, column=0, columnspan=5)

        # self.modif = Button(text="Modification", command=self.modifier_carte)
        # self.modif.grid(row=3, column=1, columnspan=5)

        # self.supp = Button(text="Suppression", command=self.supprimer_carte)
        # self.supp .grid(row=3, column=2, columnspan=5)
        self.flip_timer = window.after(3000, func=self.flip_card)
        self.next_card(window)
        # label1 = Label(self.window, text="Enter value recto:")
        # label1.pack()
        print("windoow showed")
        #self.get_window().mainloop()
        window.mainloop

    
        
    def is_known(self,window):
        # Load the CSV file into a DataFrame
        data = pd.read_csv(self.data_file)
        # Update the relevant row
        self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'correct'] += 1  

        response_quality = self.calculate_responseQuality(self.current_card['correct']+1, self.current_card['repetition']+1)
        self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'responseQuality'] = int(response_quality)
        
        
        if self.current_card['repetition'] == 0:
            review = SMTwo.first_review(5,now)

            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'nextTime'] = review.review_date
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'interval'] = review.interval
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'easiness'] = review.easiness
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'repetitions_rev'] = review.repetitions
        else:
            easiness = float(self.current_card['easiness'])
            interval = int(self.current_card['interval'])
            repetitions = int(self.current_card['repetitions_rev'])
            review = SMTwo(easiness, interval, repetitions).review(response_quality, self.current_card['nextTime'])
            
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'nextTime'] = review.review_date
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'interval'] = review.interval
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'easiness'] = review.easiness
            self.data.loc[self.data[self.recto] == self.current_card[self.recto], 'repetitions_rev'] = review.repetitions

        data.to_csv(self.data_file, index=False)
        # index = false discrads the index numbers

        history = open(self.history, 'a',newline='')
        writer = csv.writer(history)
        data = [self.current_card[self.recto], self.current_card[self.verso],now]
        writer.writerow(data)
        history.close()

        
        self.next_card(window)

    def playHangMan(self):
       csvFile=self.label+'.csv'
       HangMan(csvFile)
    def graph_correct(self):
        
        column_index = 2
        x = []
        y = []
        value_counts = Counter()

        with open('history.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                try:
                    value = datetime.datetime.strptime(row[column_index], "%Y-%m-%d").date()
                    value_counts[value] += 1
                except (IndexError, ValueError) as e:
                    print(f"Error: {e}")

        x = sorted(value_counts.keys())
        y = [value_counts[key] for key in x]
        print(x)
        print(y)
        fig = plt.figure()
        plt.plot(x, y, marker='o')
        plt.xlabel('jour')
        plt.ylabel('Nombre de mots')
        plt.title('Performance par jour')
        plt.xticks(rotation=90)
        plt.show()

        # create a canvas widget for the graph
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        # embed the canvas widget in the dashboard window
        canvas.get_tk_widget().pack()


    def graph_level(self):
        column_index = 9
        x = []
        y = []
        value_counts = Counter()

        with open(self.data_file, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            headers = next(plots)
            for row in plots:
                try:
                    value = row[column_index]
                    print(value)
                    value_counts[value] += 1
                except (IndexError, ValueError) as e:
                    print(f"Error: {e}")

        x = sorted(value_counts.keys())
        y = [value_counts[key] for key in x]
        print(x)
        print(y)
        fig = plt.figure()
        plt.plot(x, y, marker='o')
        plt.xlabel('Niveaux')
        plt.ylabel('Nombre de mots')
        plt.title('Niveau de maitrise')

        # create a canvas widget for the graph
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        # embed the canvas widget in the dashboard window
        canvas.get_tk_widget().pack()
        #plt.show()

    def dashboard(self):
        global root
        root = Tk()
        root.geometry("1250x650")

        # create a label widget and pack it at the top of the window
        label = Label(root, text="My Dashboard", font=("Arial", 24))
        label.pack(side="top", fill="x")

        # create a figure with three subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 8))


        # plot the first graph on the first subplot
        column_index1 = 2
        x1 = []
        y1 = []
        value_counts1 = Counter()

        with open(self.history, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                try:
                    value = datetime.datetime.strptime(row[column_index1], "%Y-%m-%d").date()
                    value_counts1[value] += 1
                except (IndexError, ValueError) as e:
                    print(f"Error: {e}")

        x1 = sorted(value_counts1.keys())
        y1 = [value_counts1[key] for key in x1]
        ax1.plot(x1, y1, marker='o')
        ax1.set_xlabel('jour')
        ax1.set_ylabel('Nombre de cartes')
        ax1.set_title('Questions répondu correctement par jours')
        ax1.tick_params(axis='x', rotation=90)

        # plot the second graph on the second subplot
        column_index2 = 9
        x2 = []
        y2 = []
        value_counts2 = Counter()

        with open(self.data_file, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            headers = next(plots)
            for row in plots:
                try:
                    value = row[column_index2].strip()
                    value_counts2[value] += 1
                except (IndexError, ValueError) as e:
                    print(f"Error: {e}")

        x2 = sorted(value_counts2.keys())
        y2 = [value_counts2[key] for key in x2]
    

        # plot the pie chart on the third subplot
        
        ax2.pie(y2, labels=x2, autopct='%1.1f%%')
        ax2.set_title('Niveaux de maitrise')
        ax2.legend(title = "Niveaux:")

        # create a canvas widget for the figure
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        # embed the canvas widget in the dashboard window
        canvas.get_tk_widget().pack(side="left", padx=10, pady=20)

        
        total_cards = len(pd.read_csv(self.data_file))


        # create a canvas widget for the figure
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        # calculate the percentage of cards with level 5
        summ = sum(value_counts2.values())
        if summ == 0:
            percent_level_5 = 0
        else:
            percent_level_5 = (value_counts2.get('5', 0) / summ) * 100
            percent_level_5 = round(percent_level_5, 1)

        # create a label widget for the statistic
        stat_label = Label(root, text=f"Nombre \n total \n des cartes:\n{total_cards}\n\n --------------- \n \n Cartes \n maitrisees :\n{percent_level_5:.2f}%", font=("Arial", 12))
        stat_label.pack(side="right", padx=10, pady=20)


        # embed the canvas widget and the statistic and percentage labels in the dashboard window
        canvas.get_tk_widget().pack(side="left", padx=20, pady=20)
        stat_label.pack(side="right", padx=25, pady=0)

        # embed the canvas widget and the statistic label in the dashboard window
        canvas.get_tk_widget().pack(side="left", padx=20, pady=20)


        # run the tkinter event loop
        root.mainloop() 
        
    def ajouter_carte(self):
        root = Tk()
        root.title("Ajouter carte")
        root.geometry("700x250")

        label1 = Label(root, text="Enter value recto:")
        label1.pack()
        recto = Entry(root)
        recto.pack()

        label2 = Label(root, text="Enter value verso:")
        label2.pack()
        verso = Entry(root)
        verso.pack()

        submit_button = Button(root, text="Submit", command=lambda: (self.write_card(recto.get(), verso.get()), root.destroy()))
        submit_button.pack()

        root.mainloop()


    def write_card(self, recto, verso):
        
        with open(self.data_file, mode='a', newline='') as file:
        # create a CSV writer object
            writer = csv.writer(file)
            
            # write the new row to the CSV file
            new_row = [recto,verso]
            writer.writerow(new_row)

    def modifier_carte(self):
              
        # Create the main window
        root = Tk()
        root.title("Flashcard App - Modification")
        #root.geometry("300x600")

        # Define the colors list
        colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "black"]

        # Create a function to handle button clicks

        # Create a frame to hold the three sections
        sections_frame = Frame(root)
        sections_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the first section with a label, combobox, and button
        section1_frame = Frame(sections_frame, borderwidth=2, relief="groove")
        section1_frame.pack(fill="both", expand=True, padx=10, pady=4)
        section1_label = Label(section1_frame, text="Modification du nom de la Flashcard",font=("Courrier", 10))
        section1_label.pack(padx=10, pady=4)
        section1_label1 = Label(section1_frame, text="Veuillez entrer le nouveau nom")
        section1_label1.pack(padx=10, pady=4)
        section1_entry = Entry(section1_frame)
        section1_entry.pack(padx=10, pady=4)
        section1_button = Button(section1_frame, text="Changer nom", command=lambda: (self.change_title(section1_entry.get()), section1_result_label.config(text="Nom changé avec succès !")))
        section1_button.pack(padx=10, pady=4)
        section1_result_label = Label(section1_frame, text="")
        section1_result_label.pack(padx=10, pady=10)


        # Create the second section with a label, combobox, and button
        section2_frame = Frame(sections_frame, borderwidth=2, relief="groove")
        section2_frame.pack(fill="both", expand=True, padx=10, pady=4)
        section2_label = Label(section2_frame, text="Modification de la couleur de la Flashcard",font=("Courrier", 10))
        section2_label.pack(padx=10, pady=4)
        section2_label1 = Label(section2_frame, text="Veuillez choisir la nouvelle couleur")
        section2_label1.pack(padx=10, pady=4)
        section2_combobox = ttk.Combobox(section2_frame, values=colors)
        section2_combobox.pack(padx=10, pady=4)
        section2_button = Button(section2_frame, text="Changer couleur", command=lambda: (self.change_color(section2_combobox.get()), section2_result_label.config(text="Couleur changée avec succès !")))
        section2_button.pack(padx=10, pady=4)
        section2_result_label = Label(section2_frame, text="")
        section2_result_label.pack(padx=10, pady=4)

        cartes = self.data.iloc[:, 0].tolist()

        # Create the third section with a label, combobox, and button
        section3_frame = Frame(sections_frame, borderwidth=2, relief="groove")
        section3_frame.pack(fill="both", expand=True, padx=10, pady=4)
        section3_label = Label(section3_frame, text="Modification d'une carte de la Flashcard",font=("Courrier", 10))
        section3_label.pack(padx=10, pady=4)
        section3_label1 = Label(section3_frame, text="Veuillez choisir la carte à changer")
        section3_label1.pack(padx=10, pady=4)
        section3_combobox = ttk.Combobox(section3_frame, values=cartes)
        section3_combobox.pack(padx=10, pady=4)
        section3_label2 = Label(section3_frame, text="Veuillez entrer le recto de la carte à changer")
        section3_label2.pack(padx=10, pady=4)
        section3_entry1 = Entry(section3_frame)
        section3_entry1.pack(padx=10, pady=4)
        section3_label3 = Label(section3_frame, text="Veuillez entrer le verso de la carte à changer")
        section3_label3.pack(padx=10, pady=4)
        section3_entry2 = Entry(section3_frame)
        section3_entry2.pack(padx=10, pady=4)
        section3_button = Button(section3_frame, text="Changer carte", command=lambda: (self.change_card(section3_combobox.get(),section3_entry1.get(),section3_entry2.get()), section3_result_label.config(text="Carte changée avec succès !")))
        section3_button.pack(padx=10, pady=4)
        section3_result_label = Label(section3_frame, text="")
        section3_result_label.pack(padx=10, pady=4)

        # Create an exit button
        exit_button = Button(root, text="Exit", command=root.destroy)
        exit_button.pack(side="bottom", padx=10, pady=4)

        # Start the main event loop
        root.mainloop()



    def change_title(self,new_title):
        if new_title != '':
            title = self.label
            with open("flashcards.csv", mode='r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)  # read the remaining rows
            with open("flashcards.csv", mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                # Loop through each row in the CSV file
                for row in rows:
                    if row[2] == title:
                        row[2] = new_title
                        os.rename(row[4], new_title+'.csv')
                        row[4] = new_title+'.csv'
                        os.rename(row[5], new_title+'_history.csv')
                        row[5] = new_title+'_history.csv'
                    # Write the updated row to the new CSV file
                    print(row)
                    writer.writerow(row)

    def change_color(self,new_color):
        if new_color != '':
            color = self.color
            with open("flashcards.csv", mode='r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)  # read the remaining rows
            with open("flashcards.csv", mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                # Loop through each row in the CSV file
                for row in rows:
                    print(row)
                    if row[3] == color:
                        row[3] = new_color
                        
                    # Write the updated row to the new CSV file
                    print(row)
                    writer.writerow(row)

    def change_card(self,recto,new_recto,new_verso):

        with open(self.data_file, mode='r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # read the header row
            rows = list(reader)  # read the remaining rows

        with open(self.data_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write the header row
            writer.writerow(header)

            # Loop through each row in the CSV file
            for row in rows:
                if row[0] == recto:
                    # This row corresponds to the flashcard with the specified recto value
                    # Replace the values in this row with the new values
                    row[0] = new_recto
                    row[1] = new_verso

                # Write the updated row to the new CSV file
                writer.writerow(row)
    
    def supprimer_carte(self):
        print("Supprimer arte")
        root = Tk()
        root.title("Supprimer carte")
        root.geometry("700x250")
        cartes = self.data.iloc[:, 0].tolist()
        label1 = Label(root, text="Veuillez choisir la valeur recto de la carte que vous voulez supprimer:")
        label1.pack()
        recto = ttk.Combobox(root,values=cartes)
        recto.pack(padx=10, pady=4)
        result_label = Label(root, text="")
        result_label.pack(padx=10, pady=4)
        submit_button = Button(root, text="Submit", command=lambda: (self.remove_card(recto.get()),result_label.config(text="Carte supprimée avec succès !"), root.destroy()))
        submit_button.pack()
        root.mainloop()

    def remove_card(self,recto):
        print("remove card")
        """Removes a flashcard with the specified recto value from the deck and the corresponding line from the CSV file."""
        # Remove the flashcard from the deck
        for card in self.cards:
            if card[self.verso] == recto:
                self.cards.remove(card)
                break
        
        # Remove the corresponding line from the CSV file
        with open(self.data_file, mode='r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # read the header row
            rows = list(reader)  # read the remaining rows

        with open(self.data_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write the header row
            writer.writerow(header)

            # Loop through each row in the CSV file
            for row in rows:
                if row[0] == recto:
                    # This row corresponds to the flashcard with the specified recto value
                    continue  # skip this row

                # Write the row to the new CSV file
                writer.writerow(row)

    # def hangman(self):
    #     score = 0
    #     run = True

    #     # main loop
    #     while run:
    #         root = Tk()
    #         root.geometry('905x600')
    #         root.title('HANG MAN')
    #         root.config(bg = '#E7FFFF')
    #         count = 0
    #         win_count = 0

    #         # choosing word
    #         with open(self.data_file) as f:
    #             l= csv.reader(f)
    #             rows = list(l)
    #             random_row = random.choice(rows)
    #             selected_word=random_row[1]
    #             toGuess=random_row[0]
            
            
    #         # creation of word dashes variables
    #         x = 250
    #         for i in range(0,len(selected_word)):
    #             x += 60
    #             exec('d{}=Label(root,text="_",bg="#E7FFFF",font=("arial",20))'.format(i))
    #             exec('d{}.place(x={},y={})'.format(i,x,350))
                
    #         #letters icon
    #         al = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    #         for let in al:
    #             exec('{}=PhotoImage(file="{}.png")'.format(let,let))
                
    #         # hangman images
    #         h123 = ['h1','h2','h3','h4','h5','h6','h7']
    #         for hangman in h123:
    #             exec('{}=PhotoImage(file="{}.png")'.format(hangman,hangman))
                
    #         #letters placement
    #         button = [['b1','a',0,470],['b2','b',70,470],['b3','c',140,470],['b4','d',210,470],['b5','e',280,470],['b6','f',350,470],['b7','g',420,470],['b8','h',490,470],['b9','i',560,470],['b10','j',630,470],['b11','k',700,470],['b12','l',770,470],['b13','m',840,470],['b14','n',0,530],['b15','o',70,530],['b16','p',140,530],['b17','q',210,530],['b18','r',280,530],['b19','s',350,530],['b20','t',420,530],['b21','u',490,530],['b22','v',560,530],['b23','w',630,530],['b24','x',700,530],['b25','y',770,530],['b26','z',840,530]]

    #         for q1 in button:
    #             exec('{}=Button(root,bd=0,command=lambda:check("{}","{}"),bg="#E7FFFF",activebackground="#E7FFFF",font=10,image={})'.format(q1[0],q1[1],q1[0],q1[1]))
    #             exec('{}.place(x={},y={})'.format(q1[0],q1[2],q1[3]))
                
    #         #hangman placement
    #         han = [['c1','h1'],['c2','h2'],['c3','h3'],['c4','h4'],['c5','h5'],['c6','h6'],['c7','h7']]
    #         for p1 in han:
    #             exec('{}=Label(root,bg="#E7FFFF",image={})'.format(p1[0],p1[1]))

    #         # placement of first hangman image
    #         c1.place(x = 300,y =- 50)
            
    #         #exit button
    #         def close():
    #             global run
    #             answer = messagebox.askyesno('ALERT','YOU WANT TO EXIT THE GAME?')
    #             if answer == True:
    #                 run = False
    #                 root.destroy()
                    
    #         e1 = PhotoImage(file = 'exit.png')
    #         ex = Button(root,bd = 0,command = close,bg="#E7FFFF",activebackground = "#E7FFFF",font = 10,image = e1)
    #         ex.place(x=770,y=10)
    #         s2 = 'SCORE:'+str(score)
    #         s1 = Label(root,text = s2,bg = "#E7FFFF",font = ("arial",25))
    #         s1.place(x = 10,y = 10)
    #         tentatives=str(6-count)
    #         s3 = Label(root,text='-----------------------------\n Vous avez '+tentatives+' tentatives\n pour trouver l\'équivalent  \n du mot suivant: \n"'+toGuess+'"\n-----------------------------',
    #                 bg = "black",
    #                 fg="white",
    #                 font = ("arial",25))
    #         s3.place(x = 10,y = 100)
    #         # button press check function
    #         def check(letter,button):
    #             global count,win_count,run,score
    #             exec('{}.destroy()'.format(button))
    #             if letter in selected_word:
    #                 for i in range(0,len(selected_word)):
    #                     if selected_word[i] == letter:
    #                         win_count += 1
    #                         exec('d{}.config(text="{}")'.format(i,letter.upper()))
    #                 if win_count == len(selected_word):
    #                     score += 1
    #                     answer = messagebox.askyesno('GAME OVER','YOU WON!\nWANT TO PLAY AGAIN?')
    #                     if answer == True:
    #                         run = True
    #                         root.destroy()   
    #                     else:
    #                         run = False
    #                         root.destroy()
    #             else:
    #                 count += 1
    #                 exec('c{}.destroy()'.format(count))
    #                 exec('c{}.place(x={},y={})'.format(count+1,300,-50))
    #                 if count == 6:
    #                     answer = messagebox.askyesno('GAME OVER','YOU LOST!\nWANT TO PLAY AGAIN?')
    #                     if answer == True:
    #                         run = True
    #                         score = 0
    #                         root.destroy()
    #                     else:
    #                         run = False
    #                         root.destroy()         
    #         root.mainloop()



    @staticmethod
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



 # create instance d'objet Flashcard
# flashcard_fr_eng = Flashcard('frToEng','English','French',"white",'frToEng.csv','frToEng_history.csv')
# # flashcard_fr_eng.supprimer_carte()
# flashcard_fr_eng.show_window()

        
