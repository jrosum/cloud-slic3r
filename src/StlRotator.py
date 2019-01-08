import os
import time

from stltweak import FileHandler
from stltweak.MeshTweaker import Tweak


class StlRotator:
    def __init__(self):
        print("StlRotator Loaded")
        self.fileHandler = FileHandler.FileHandler()

    def rotate(self, filepath, outputfile, convert):

        ## Get the command line arguments. Run in IDE for demo tweaking.
        stime = time.time()

        try:
            # print(args.inputfile)
            objs = self.fileHandler.loadMesh(filepath)

        except(KeyboardInterrupt, SystemExit):
            print("\nError, loading mesh from file failed!")
            raise

        c = 0
        for obj in objs:
            mesh = obj["Mesh"]
            if convert:
                R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            else:
                try:
                    cstime = time.time()
                    x = Tweak(mesh, True, True, 0)
                    R = x.R
                except (KeyboardInterrupt, SystemExit):
                    print("\nError, tweaking process failed!")
                    raise

                print("\nResult-stats:")
                print(" Tweaked Z-axis: \t{}".format((x.Zn)))
                print(" Axis, angle:   \t{v}, {phi}".format(v=x.v, phi=x.phi))
                print(""" Rotation matrix: 
                {:2f}\t{:2f}\t{:2f}
                {:2f}\t{:2f}\t{:2f}
                {:2f}\t{:2f}\t{:2f}""".format(x.R[0][0], x.R[0][1], x.R[0][2],
                                              x.R[1][0], x.R[1][1], x.R[1][2],
                                              x.R[2][0], x.R[2][1], x.R[2][2]))
                print(" Unprintability: \t{}".format(x.Unprintability))

                print("\nFound result:    \t{:2f} s".format(time.time() - cstime))

                ## Creating tweaked output file
            if os.path.splitext(outputfile)[1].lower() in ["stl", ".stl"]:
                # If you want to write in binary, use the function rotatebinSTL(...)"
                tweakedcontent = self.fileHandler.rotateSTL(R, mesh, filepath)
                # Support structure suggestion can be used for further applications
                # if x.Unprintability > 7:
                #    tweakedcontent+=" {supportstructure: yes}"
                if len(objs) <= 1:
                    outfile = outputfile
                else:
                    outfile = os.path.splitext(outputfile)[0] + " ({})".format(c) + \
                              os.path.splitext(outputfile)[1]
                with open(outfile, 'w') as outfile:  # If you want to write in binary, open with "wb"
                    outfile.write(tweakedcontent)

            else:
                transformation = "{} {} {} {} {} {} {} {} {} 0 0 1".format(x.R[0][0], x.R[0][1], x.R[0][2],
                                                                           x.R[1][0], x.R[1][1], x.R[1][2],
                                                                           x.R[2][0], x.R[2][1], x.R[2][2])
                obj["transform"] = transformation
                self.fileHandler.rotate3MF(filepath, outputfile, objs)

                ## Success message
            print("Tweaking took:  \t{:2f} s".format(time.time() - stime))
            print("\nSuccessfully Rotated!")
