import tkinter as tk
from tkinter import ttk
import random
from tkinter import *
import pandas as pd
import re
LARGEFONT =("Verdana", 35)

def is_comprehensible(word_f, word_e):
        if not re.match("^[a-zA-Z]+$", word_f) or not re.match("^[a-zA-Z]+$", word_e) or word_f.lower() == word_e.lower():
            return False
        return True

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1, Page2):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
		
		# putting the grid in its place by using
		# grid
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		button1 = ttk.Button(self, text ="Page 1",
		command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		## button to show frame 2 with text layout2
		button2 = ttk.Button(self, text ="Page 2",
		command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		


# second window frame page1
class Page1(tk.Frame):
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


  
    BACKGROUND_COLOR = "#B1DDC6"
    data_comprehensible = data[data.apply(lambda x:is_comprehensible(x['French'], x['English']), axis=1)]
    data_comprehensible.to_csv("frToEng_comprehensible.csv", index=False)
    to_learn = data.to_dict(orient="records")

    # Define a function to check if a word is comprehensible

    # Filter out the words that are not comprehensible
    



    def is_comprehensible(word_f, word_e):
        if not re.match("^[a-zA-Z]+$", word_f) or not re.match("^[a-zA-Z]+$", word_e) or word_f.lower() == word_e.lower():
            return False
        return True

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
      # index = false discrads the index numbers
      next_card()
     
    def __init__(self, parent, controller):
        BACKGROUND_COLOR = "#B1DDC6" 
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Flashcard App", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        #ttk.config(padx=50, pady=50, bg=BACKGROUND_COLOR)!!!
        #flip_timer = tk.after(3000, func=flip_card) # 3000 milliseocnds = 3 seconds

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
        # layout2

		# using grid
	



# third window frame page2
class Page2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Page 1",
							command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


# Driver Code
app = tkinterApp()
app.mainloop()
