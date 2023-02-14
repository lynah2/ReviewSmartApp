import csv
import random
from datetime import date, timedelta

start_date = date(2023, 1, 1)  # start date: January 1st, 2023
end_date = date(2023, 2, 1)  # end date: February 1st, 2023

date_list = []
current_date = start_date
while current_date < end_date:
    date_list.append(current_date)
    current_date += timedelta(days=1)

rows = []
with open('frToEng_comprehensible.csv', 'r') as inputfile:
    reader = csv.reader(inputfile)
    header = next(reader)  # skip the header row
    for row in reader:
        rows.append(row)

random_rows = random.sample(rows, 100)  # select 100 random rows from the input file

with open('Learn_words2.csv', 'a', newline='') as outputfile:
    writer = csv.writer(outputfile)
    #writer.writerow(header + ['date'])  # write the header row with the new "date" column
    for row in random_rows:
        random_date = random.choice(date_list)  # select a random date from the date list
        writer.writerow(row + [random_date.strftime('%Y-%m-%d')])
