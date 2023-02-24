from tkinter import *
from PIL import Image, ImageTk
import subprocess

BACKGROUND_COLOR = "#050D54"


def aide(root):
    sub_window = Toplevel(root)
    sub_window.title("Flashcard App - Aide!")
    sub_window.config(bg=BACKGROUND_COLOR)
    #sub_window.geometry("600x600")
    label = Label(sub_window, text="Comment fonctionne notre application?",font=("Courrier", 28),bg=BACKGROUND_COLOR,fg="white")
    label.pack()
    # Create a frame to hold the three sections
    sections_frame = Frame(sub_window)
    sections_frame.pack(fill="both", expand=True, padx=10, pady=4)
    sections_frame.config(bg=BACKGROUND_COLOR)

    section1_frame = Frame(sections_frame, borderwidth=2, relief="groove")
    section1_frame.pack(fill="both", expand=True, padx=10, pady=4)
    
    section1_label = Label(section1_frame, text="Objectif",font=("Courrier", 18), anchor="w",bg=BACKGROUND_COLOR,fg="white")
    section1_label.pack(padx=10, pady=4)
    section1_label1 = Label(section1_frame, text="Notre application a pour objectif de faciliter la mémorisetion de nouvelles informations en se basant sur un système de répétition espacée (SPACED REPETITION).",bg=BACKGROUND_COLOR,fg="white")
    section1_label1.pack(padx=10, pady=4)
    section1_frame.config(bg=BACKGROUND_COLOR)
    # Create the second section with a label, combobox, and button
    section2_frame = Frame(sections_frame, borderwidth=2, relief="groove")
    section2_frame.pack(fill="both", expand=True, padx=10, pady=4)
    
    section2_label = Label(section2_frame, text="Comment procéder?",font=("Courrier", 18),bg=BACKGROUND_COLOR,fg="white")
    section2_label.pack(padx=10, pady=4)
    section2_label1 = Label(section2_frame, text="On vous propose une Flashcard pour apprendre l'Anglais, mais vous pouvez tous de même créer vos propres cartes personnalisés.",bg=BACKGROUND_COLOR,fg="white")
    section2_label1.pack(padx=10, pady=4)
    section2_frame.config(bg=BACKGROUND_COLOR)
    
    


    # Create the third section with a label, combobox, and button
    section3_frame = Frame(sections_frame, borderwidth=2, relief="groove")
    section3_frame.pack(fill="both", expand=True, padx=10, pady=4)
    section3_label = Label(section3_frame, text="Evaluation",font=("Courrier", 18),bg=BACKGROUND_COLOR,fg="white")
    section3_label.pack(padx=10, pady=4)
    section3_label1 = Label(section3_frame, text="Pour permettre à l'utilisateur de mesurer sa progression, on propose un système d'évaluation comme suit:",bg=BACKGROUND_COLOR,fg="white")
    section3_label1.pack(padx=10, pady=4)
    text = Text(section3_frame, state="disabled", height=8, width=80,bg=BACKGROUND_COLOR,fg="white")
    text.pack()
    text.config(state="normal")
    # Insert text with bullets
    text.insert(END, "\u2022 Niveau Maitrise 5: Vous connaissez la réponse sans hésitation.\n")
    text.insert(END, "\u2022 Niveau Bon 4: Vous connaissez la réponse, mais cela prend un peu plus de temps pour se rappeler.\n")
    text.insert(END, "\u2022 Niveau Pass 3: Vous êtes sur la bonne voie, mais vous avez besoin d'un indice pour vous rappeler de la réponse.\n")
    text.insert(END, "\u2022 Niveau Fail 2: Vous avez du mal à vous rappeler de la réponse\n")
    text.insert(END, "\u2022 Niveau Médiocre 1:  Vous ne connaissez pas la réponse du tout et vous devez réviser la carte plus souvent.\n")

    # Set state back to "disabled" to prevent user editing
    text.config(state="disabled")

    section3_frame.config(bg=BACKGROUND_COLOR)
    
    

    # Create an exit button
    exit_button = Button(sub_window, text="Exit", command=sub_window.destroy)
    exit_button.pack(side="bottom", padx=10, pady=4)


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
button =Button(root,text='Aide',font=("Courrier", 14, 'bold'),width=15,bg='#FAD727',fg='white',height=2, borderwidth=0, cursor='hand2', border='0', command=lambda: (aide(root)))
button.config()
button.place( x=330, y=477)

root.mainloop()
