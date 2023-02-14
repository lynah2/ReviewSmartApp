import matplotlib.pyplot as plt
import csv
import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

x = []
y = []

column_index = 2  # 0-based index of the column you want to count
value_counts = Counter()

with open('learn_words2.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    headers = next(plots)
    for row in plots:
        print(row)  # print the contents of the row
        try:
            value = datetime.datetime.strptime(row[column_index], "%Y-%m-%d").date()
            value_counts[value] += 1
        except (IndexError, ValueError) as e:
            print(f"Error: {e}")
        #value = datetime.datetime.strptime(row[column_index], "%Y-%m-%d").date()
        #value = row[column_index]
        #value_counts[value] += 1
        #date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
        #x.append(date)
        #y.append(float(row[0]))

#x=list(value_counts.keys())
#y=list(value_counts.values())
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

root = tk.Tk()
root.title("Graph")

canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root.mainloop()
