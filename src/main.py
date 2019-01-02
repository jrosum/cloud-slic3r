from flask import Flask, render_template, request, send_file, abort, send_from_directory
from os import system, makedirs, chdir
from Render import Render
from glob import glob
import zipfile
from random import random
from stltools import stl, utils
import stl as stl_numpy
from stl import mesh
from RepairStl import RepairStl
from SendToPrinter import SendToPrinter

app = Flask(__name__)
render = Render(system, random, stl, utils, mesh, stl_numpy)
repair_stl = RepairStl(system)

api_key = "1f203e90-10c9-4e1a-ab1b-40f43c220f43"
host = "druckerei.synyx.coffee"
printer_name = "Prusa_i3"

send_to_printer = SendToPrinter(system, host, printer_name, api_key)

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
    folder_id = str(int(random() * 1000))
    folder_name = "./temp/{}/".format(folder_id)
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
        repair_stl.repair_and_save_ascii(folder_name, input_file_name)
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
            return render_template("uploader.html", temp_folder = folder_id)
        except Exception as e:
            print(e)
            return abort(500)
    else:
        return abort(500)


def get_zip_file_path(folder_id):
    path = "./temp/{}".format(folder_id)
    chdir(path)
    zip_file_name = glob("*.zip")[0]
    return "{}/{}".format(path, zip_file_name)

def get_gcode_file_path(folder_id):
    path = "./temp/{}".format(folder_id)
    chdir(path)
    gcode_file_name = glob("*.gcode")[0]
    return "{}/{}".format(path, gcode_file_name)

@app.route('/vorschau/<folder_id>/preview.png', methods=['GET'])
def get_png_file(folder_id):
    path = "./temp/{}".format(folder_id)
    return send_from_directory(path, "preview.png")

@app.route('/download/<folder_id>', methods=['GET'])
def download_zip(folder_id):
    try:
        int(folder_id)
        try:
            send_to_printer.upload(get_gcode_file_path(folder_id))
            path = get_zip_file_path(folder_id)
            print("Try to download {}".format(path))
            return send_file(path, as_attachment=True)
        except Exception as e:
            print(e)
            return abort(404)
    except:
        return abort(400)


if __name__ == '__main__':

    makedirs("./temp", exist_ok=True)
    app.run("0.0.0.0", 8088, debug=True)