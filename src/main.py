from flask import Flask, render_template, request, send_file, abort
from os import system, makedirs
from Render import Render
import zipfile
from random import random
from stltools import stl, utils
import stl as stl_numpy
from stl import mesh

app = Flask(__name__)
render = Render(system, random, stl, utils, mesh, stl_numpy)


def slic3r_command(file, height, support, gcode_name):
    if support == "on":
        command = "slic3r " + file + \
                  " --nozzle-diameter 0.4" \
                  " --filament-diameter 1.75 " \
                  " --temperature 200 " \
                  " --bed-temperature 60 " \
                  " --layer-height " + str(height) + " " \
                  " --support-material " \
                  "--output " + gcode_name + " " \
                  " && rm *.stl "
    else:
        command = "slic3r " + file + \
                  " --nozzle-diameter 0.4" \
                  " --filament-diameter 1.75 " \
                  " --temperature 200 " \
                  " --bed-temperature 60 " \
                  " --layer-height " + str(height) + " " \
                  "--output " + gcode_name + " " \
                  " && rm *.stl "

    return command

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    folder_name = "./temp/" +str(int(random() * 1000)) + "/"
    makedirs(folder_name)
    f = request.files['file']
    form = request.form
    input_file_name = "input.stl"

    if "height" in form.keys() or not form["height"] == "":
        height = form["height"]
    else:
        return abort(400)

    if "support" in form.keys():
        support = request.form["support"]
    else:
        support = "off"

    filename_check = "&&" in f.filename or "|" in f.filename

    if not filename_check :
        print("received: " + f.filename)
        f.save(folder_name + input_file_name)
        image_name = render.render_stl(folder_name, input_file_name)
        gcode = folder_name + str(f.filename).split(".")[0] +".gcode"
        system(slic3r_command(folder_name + input_file_name, height, support, gcode))

        try:
            zip_name = folder_name + str(f.filename).split(".")[0] + ".zip"
            print("Sending" + gcode)
            zip = zipfile.ZipFile(zip_name, "w")
            zip.write(gcode)
            zip.write(folder_name + image_name)
            zip.close()
            return send_file(zip_name, as_attachment=True)
        except Exception as e:
            print(e)
            return abort(500)
    else:
        return abort(500)

if __name__ == '__main__':

    makedirs("./temp", exist_ok=True)
    app.run("0.0.0.0", 8088, debug=True)