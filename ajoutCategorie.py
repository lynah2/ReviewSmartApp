import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import csv

BACKGROUND_COLOR = "#050D54"


def save_to_csv():
    data = [rectoCarte_entry.get(), versoCarte_entry.get(), Categorie_entry.get(), Calor_combobox.get(),Categorie_entry.get()+'.csv',Categorie_entry.get()+'_history.csv']
    if not all(data):
        window.destroy()
    else:
        with open('flashcards.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)
        labels=[data[0],data[1]]
        with open(Categorie_entry.get()+'.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(labels)
        with open(Categorie_entry.get()+'_history.csv', 'a', newline="") as file:
            writer = csv.writer(file)
        window.destroy()

window = tkinter.Tk()
window.title("Flashcard App - Ajout d'une Nouvelle Flashcard")
window.config(bg=BACKGROUND_COLOR)

frame = tkinter.Frame(window)
frame.pack()
frame.config(bg=BACKGROUND_COLOR)

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text="Informations sur la Nouvelle Flashcard",bg=BACKGROUND_COLOR,fg="white")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)
user_info_frame.config(bg=BACKGROUND_COLOR)

Categorie_label = tkinter.Label(user_info_frame, text="Label de la flashcard",bg=BACKGROUND_COLOR,fg="white")
Categorie_entry = ttk.Entry(user_info_frame)
Categorie_label.grid(row=0, column=0)
Categorie_entry.grid(row=1, column=0)

rectoCarte_label = tkinter.Label(user_info_frame, text="Label du recto de la carte",bg=BACKGROUND_COLOR,fg="white")
rectoCarte_label.grid(row=0, column=1)
versoCarte_label = tkinter.Label(user_info_frame, text="Label du verso de la carte",bg=BACKGROUND_COLOR,fg="white")
versoCarte_label.grid(row=0, column=2)

rectoCarte_entry = tkinter.Entry(user_info_frame)
versoCarte_entry = tkinter.Entry(user_info_frame)
rectoCarte_entry.grid(row=1, column=1)
versoCarte_entry.grid(row=1, column=2)

colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "black"]
Calor_label = tkinter.Label(user_info_frame, text="Couleur",bg=BACKGROUND_COLOR,fg="white")
Calor_combobox = ttk.Combobox(user_info_frame, values=colors)
Calor_label.grid(row=2, column=0)
Calor_combobox.grid(row=3, column=0)
Calor_combobox.set("green")


for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
# Button
button = tkinter.Button(frame, text="Ajouter", command= save_to_csv,bg="orange",fg="white")
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

window.mainloop()

