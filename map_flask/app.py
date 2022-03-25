# to get a virtual environment, run "python3 -m venv venv" and then ". venv/bin/activate"

from flask import Flask, render_template
import csv
import threading 

app = Flask(__name__)

@app.route("/")
def main():
    with open("map_flask/data.csv", mode="r", encoding="utf-8-sig") as csv_file: #had to use relative path
        csv_reader = csv.reader(csv_file)
        markers = []
        for row in csv_reader: 
            markers.append([float(row[1]), float(row[2])])
            print(markers)
    
        with app.app_context(): # got the idea from stack exchange
            if (len(markers) < 10):
                return render_template('map.html', markers=markers)
            else:
                return render_template('map.html', markers=markers[:10])

def update():
  threading.Timer(5.0, update).start()
  main()
  app.run()

if __name__ == "__main__":
    update() # https://stackoverflow.com/questions/52581576/could-not-import-d-flask-app


