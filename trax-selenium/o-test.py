from urllib import request
import re
import csv

csv_file = csv.reader(open("duitouSKU.csv", "r"))

print(csv_file)

for item in csv_file:
    print(item[0])

