import tkinter as tk

class Deck:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.occ = {} # dictionnaire pour stocker les Decks
        
        # creation label et entry
        self.label = tk.Label(fenetre, text="Tapez votre ligne :", background='#CDBDE8').grid(row=0, padx=10, pady=10)
        self.occ_entry = tk.Entry(fenetre)
        self.occ_entry.grid(row=0, column=1, padx=10, pady=10)
              
        # create button 
        self.add_button = tk.Button(fenetre, text="Afficher" ,command=self.afficher)  
        self.add_button.grid(row=2, column=1)
        self.add_button.config(background='#ECE4F9')

        # creation label du resultat
        self.result_label = tk.Label(fenetre, background='#CDBDE8')
        self.result_label.grid(row=3, column=1, padx=10, pady=10)

        
    
    def afficher(self):  
        """ fonction qui calcule le nombres d'occurences des lettres """
        occ = self.occ_entry.get()    
        for t in occ:
            if t in self.occ.keys():    #lettre existe deja
                self.occ[t] += 1
            else:                         #lettre n'exite pas encore en dictionnaire
                self.occ[t] = 1 
        self.result_label.config(text=self.occ)   #affiche resultat

        
# creation fenetre tkinter
mafenetre = tk.Tk()
mafenetre.title("Calculatrice d'occurences")
mafenetre.config(background='#CDBDE8')

# create instance d'objet Occurence
occurences = Deck(mafenetre)

# Demarrage de mainloop
mafenetre.mainloop()