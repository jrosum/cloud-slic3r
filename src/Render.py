class Render:

    def __init__(self, system, random):
        self.system = system
        self.random = random
        print("render class loaded")

    def render_stl(self, filename):

        pov_file = str(self.random()) + ".pov"
        png_name = "preview_" + str(self.random()) + ".png"
        render_command = "stl2pov " + str(filename) + " > " + pov_file + " && " \
                         "povray  -i\"" + pov_file + "\" +FN +W1920 +H1080 -o\"" + png_name + "\" +Q9 +AM1 +A +UA"
        self.system(render_command)
        return png_name





