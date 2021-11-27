import csv
import hast

with open("./HAST_MATRIX.csv", 'w') as file:
    writer = csv.DictWriter(file, fieldnames=hast.standardizedScoreMatrix.keys())
    writer.writeheader()
    for i in range(66):
        writer.writerow(
            {k:v[i] for k,v in hast.standardizedScoreMatrix.items()}
        )