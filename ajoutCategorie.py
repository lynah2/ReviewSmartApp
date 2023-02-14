import tkinter
from tkinter import ttk
from tkinter import messagebox
import os
import openpyxl
from tkinter import *
import subprocess
import csv
import sys

def run_python_script():
    subprocess.Popen(["python", "enterInfoFlashCard.py"])
    sys.exit()

def save_to_csv():
    data = [Categorie_entry.get(), rectoCarte_entry.get(), versoCarte_entry.get(), Calor_combobox.get()]
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    run_python_script()

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
user_info_frame =tkinter.LabelFrame(frame, text="Information de la Nouvelle Catégorie")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

Categorie_label = tkinter.Label(user_info_frame, text="label du Catégorie")
Categorie_entry = ttk.Entry(user_info_frame)
Categorie_label.grid(row=0, column=0)
Categorie_entry.grid(row=1, column=0)

rectoCarte_label = tkinter.Label(user_info_frame, text=" label du Recto de la carte")
rectoCarte_label.grid(row=0, column=1)
versoCarte_label = tkinter.Label(user_info_frame, text="label du Verso de la carte")
versoCarte_label.grid(row=0, column=2)

rectoCarte_entry = tkinter.Entry(user_info_frame)
versoCarte_entry = tkinter.Entry(user_info_frame)
rectoCarte_entry.grid(row=1, column=1)
versoCarte_entry.grid(row=1, column=2)

colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "gray", "black", "white"]
Calor_label = tkinter.Label(user_info_frame, text="Catégorie")
Calor_combobox = ttk.Combobox(user_info_frame, values=colors)
Calor_label.grid(row=2, column=0)
Calor_combobox.grid(row=3, column=0)
Calor_combobox.set("orange")



for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
# Button
button = tkinter.Button(frame, text="Ajouter", command= save_to_csv)
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

window.mainloop()