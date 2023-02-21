import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import csv



def save_to_csv():
    data = [rectoCarte_entry.get(), versoCarte_entry.get(), Categorie_entry.get(), Calor_combobox.get(),Categorie_entry.get()+'.csv']
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

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text="Informations sur la Nouvelle Flashcard")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

Categorie_label = tkinter.Label(user_info_frame, text="Label de la flashcard")
Categorie_entry = ttk.Entry(user_info_frame)
Categorie_label.grid(row=0, column=0)
Categorie_entry.grid(row=1, column=0)

rectoCarte_label = tkinter.Label(user_info_frame, text="Label du recto de la carte")
rectoCarte_label.grid(row=0, column=1)
versoCarte_label = tkinter.Label(user_info_frame, text="Label du verso de la carte")
versoCarte_label.grid(row=0, column=2)

rectoCarte_entry = tkinter.Entry(user_info_frame)
versoCarte_entry = tkinter.Entry(user_info_frame)
rectoCarte_entry.grid(row=1, column=1)
versoCarte_entry.grid(row=1, column=2)

colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "black", "white"]
Calor_label = tkinter.Label(user_info_frame, text="Couleur")
Calor_combobox = ttk.Combobox(user_info_frame, values=colors)
Calor_label.grid(row=2, column=0)
Calor_combobox.grid(row=3, column=0)
Calor_combobox.set("white")


for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
# Button
button = tkinter.Button(frame, text="Ajouter", command= save_to_csv)
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

window.mainloop()

