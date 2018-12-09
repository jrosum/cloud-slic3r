class Render:

    def __init__(self, system):
        self.system = system
        print("render class loaded")

    def render_stl(self, filename):
        render_command = "stl2pov " + str(filename) + " > stl.pov && povray  -i\"stl.pov\" +FN +W1920 +H1080 -o\"my_model.png\" +Q9 +AM1 +A +UA"
        self.system(render_command)





