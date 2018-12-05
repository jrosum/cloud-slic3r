from flask import Flask, render_template, request, send_file, abort
from os import system
app = Flask(__name__)

def slic3r_command(file):
    return "slic3r " + file + " --nozzle-diameter 0.4" \
                                         " --filament-diameter 1.75 " \
                                         " --temperature 200 " \
                                         " --bed-temperature 60 && rm *.stl " \
                                         " --layer-height 0.1"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        system("rm *.gcode")
        f = request.files['file']
        filename_check = "&&" in f.filename or "|" in f.filename

        if not filename_check :
            f.save(f.filename)
            system(slic3r_command(str(f.filename)))
            gcode = str(f.filename).split(".")[0] + ".gcode"

            try:
                return send_file(gcode, as_attachment=True)
            except Exception as e:
                return abort(500)
        else:
            return abort(500)

if __name__ == '__main__':
    app.run("0.0.0.0", 8081)