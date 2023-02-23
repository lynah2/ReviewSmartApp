
                i+=1
                if i%3==0:
                    i=0
                    k+=1
                print(fcards)


def run_game_script():
    subprocess.call(["python", "hangman.py"])

def add_button():
    subprocess.call(["python", "ajoutCategorie.py"])
