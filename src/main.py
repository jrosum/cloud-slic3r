from flask import Flask, render_template, request, send_file, abort
from os import system
app = Flask(__name__)

def slic3r_command(file):
    return "slic3r " + file + \
                                " --nozzle-diameter 0.4" \
                                " --filament-diameter 1.75 " \
                                " --temperature 200 " \
                                " --bed-temperature 60 " \
                                " --layer-height 0.1 " \
                                "&& rm *.stl "


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
            print "received: " + f.filename
            f.save(f.filename)
            print slic3r_command(str(f.filename))
            system(slic3r_command(str(f.filename)))
            gcode = "../" + str(f.filename).split(".")[0] + ".gcode"

            try:
                print "Sending" + gcode
                return send_file(gcode, as_attachment=True)
            except Exception as e:
                print e
                return abort(500)
        else:
            return abort(500)

if __name__ == '__main__':
    app.run("0.0.0.0", 8081)