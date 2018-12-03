from flask import Flask, render_template, request, send_file
from os import system
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        system("rm *.gcode")
        f = request.files['file']
        f.save(f.filename)
        system("slic3r " + str(f.filename) + " --nozzle-diameter 0.4 --filament-diameter 1.75 --temperature 200 --bed-temperature 60 && rm *.stl")
        gcode = str(f.filename).split(".")[0] + ".gcode"
        try:
            return send_file(gcode, as_attachment=True)
        except Exception as e:
            return "Slic3r was not able to process your file"

if __name__ == '__main__':
    app.run("0.0.0.0", 80)