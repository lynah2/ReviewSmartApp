import tkinter
from tkinter import ttk
from tkinter import messagebox
import os
import openpyxl
from tkinter import *
import subprocess
import sys

def run_python_script():
    subprocess.Popen(["python", "ajoutCategorie.py"])
    sys.exit()

def enter_data():
    accepted = accept_var.get()
    
    if accepted=="Accepted":
        # User info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        
        if firstname and lastname:
            title = title_combobox.get()
            age = age_spinbox.get()
            nationality = nationality_combobox.get()
            
            # Course info
            registration_status = reg_status_var.get()
            numcourses = numcourses_spinbox.get()
            numsemesters = numsemesters_spinbox.get()
            
            print("First name: ", firstname, "Last name: ", lastname)
            print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
            print("# Courses: ", numcourses, "# Semesters: ", numsemesters)
            print("Registration status", registration_status)
            print("------------------------------------------")
            
            filepath = "D:\codefirst.io\Tkinter Data Entry\data.xlsx"
            
            if not os.path.exists(filepath):
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                heading = ["First Name", "Last Name", "Title", "Age", "Nationality",
                           "# Courses", "# Semesters", "Registration status"]
                sheet.append(heading)
                workbook.save(filepath)
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active
            sheet.append([firstname, lastname, title, age, nationality, numcourses,
                          numsemesters, registration_status])
            workbook.save(filepath)
                
        else:
            tkinter.messagebox.showwarning(title="Error", message="First name and last name are required.")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="You have not accepted the terms")

window = tkinter.Tk()
window.title("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text="Information de la Nouvelle Carte")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

rectoCarte_label = tkinter.Label(user_info_frame, text=" Recto de la carte")
rectoCarte_label.grid(row=0, column=0)
versoCarte_label = tkinter.Label(user_info_frame, text="Verso de la carte")
versoCarte_label.grid(row=0, column=1)

rectoCarte_entry = tkinter.Entry(user_info_frame)
versoCarte_entry = tkinter.Entry(user_info_frame)
rectoCarte_entry.grid(row=1, column=0)
versoCarte_entry.grid(row=1, column=1)

Categorie_label = tkinter.Label(user_info_frame, text="Catégorie")
Categorie_combobox = ttk.Combobox(user_info_frame, values=["", "fr_To_Eng"])
Categorie_label.grid(row=0, column=2)
Categorie_combobox.grid(row=1, column=2)

image_ajout=PhotoImage(file="ajoutCategories.png")
button = tkinter.Button(user_info_frame,image=image_ajout, command= run_python_script)
button.grid(row=1, column=3, sticky="news")


for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
# Button
button = tkinter.Button(frame, text="Ajouter", command= enter_data)
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

# Saving Course Info
displayInfo_frame = tkinter.LabelFrame(frame)
displayInfo_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

recto_label = tkinter.Label(displayInfo_frame, text="Recto Carte")
recto_label.grid(row=0, column=0)

verso_label = tkinter.Label(displayInfo_frame, text= "Verso Carte")
verso_label.grid(row=0, column=1)


category_label = tkinter.Label(displayInfo_frame, text="Catégorie")
category_label.grid(row=0, column=2)

action_label = tkinter.Label(displayInfo_frame, text="Action")
action_label.grid(row=0, column=3)


for widget in displayInfo_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
#
displayCategoryInfo_frame = tkinter.LabelFrame(frame)
displayCategoryInfo_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

category_label = tkinter.Label(displayCategoryInfo_frame, text="Catégorie")
category_label.grid(row=0, column=0)

recto_label = tkinter.Label(displayCategoryInfo_frame, text="label du Recto")
recto_label.grid(row=0, column=1)

verso_label = tkinter.Label(displayCategoryInfo_frame, text= "label du Verso")
verso_label.grid(row=0, column=2)


nbrCarte = tkinter.Label(displayCategoryInfo_frame, text="Nombre de Cartes")
nbrCarte.grid(row=0, column=3)

action_label = tkinter.Label(displayCategoryInfo_frame, text="Action")
action_label.grid(row=0, column=4)


for widget in displayCategoryInfo_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)




 
window.mainloop()


























'''
from  tkinter import *

mafenetre= Tk()

titre=Label(mafenetre, text='nouvel Mot')
titre.place(x=10, y=10)

Mot=Label(mafenetre, text='Mot')
Mot.place(x=10, y=50)
zone_Mot=Entry(mafenetre)
zone_Mot.place(x=10, y=60)

traduction=Label(mafenetre, text='traduction')
traduction.place(x=100, y=10)
zone_traduction=Entry(mafenetre)
zone_traduction.place(x=100, y=60)

category=Label(mafenetre, text='catégorie')
category.place(x=210, y=10)
zone_category=Entry(mafenetre)
zone_category.place(x=210, y=60)

button = Button(mafenetre, text='Ajouter')
button.place(x=300, y=100)

mafenetre.geometry("500x200")
mafenetre.mainloop()
'''