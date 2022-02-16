from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route("/")
def main():
    with open("data.csv", mode="r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file)
        markers = []
        for row in csv_reader: 
            markers.append([float(row[1]), float(row[2])])
        print(markers)
            
    return render_template('map.html', markers=markers)
