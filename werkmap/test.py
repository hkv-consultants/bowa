import csv

rows = csv.reader(open('resultaat.txt', 'rb'), delimiter=b'\t')
cols = zip(*rows)

