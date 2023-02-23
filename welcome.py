from tkinter import *
from PIL import Image, ImageTk
import subprocess

def add_button():
    subprocess.call(["python", "enterInfoFlashCard.py"])

def run_python_script():
    subprocess.call(["python", "frameColumnspanTest.py"])


root = Tk()
root.title('SmartReview')
# Set window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to full screen
root.geometry("%dx%d+0+0" % (screen_width, screen_height))



# Load image
image = Image.open("images/background.png")

# Convert image to PhotoImage object
image = ImageTk.PhotoImage(image)

# Create label and set image as its background
background_label = Label(root, image=image)
background_label.pack(fill="both", expand="yes")

#image_ajout=PhotoImage(file="commencer.png")
#image_ajout = image_ajout.subsample(2, 2)relief="raised", bd=0 
button =Button(root,text='Commmencer',font=("Courrier", 14, 'bold'),width=15,bg='#FAD727',fg='white',height=2, borderwidth=0, cursor='hand2', border='0', command=run_python_script)
button.config()
button.place( x=80, y=477)
button =Button(root,text='Aide',font=("Courrier", 14, 'bold'),width=15,bg='#FAD727',fg='white',height=2, borderwidth=0, cursor='hand2', border='0', command=add_button)
button.config()
button.place( x=330, y=477)

root.mainloop()
