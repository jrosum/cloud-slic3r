class Render:

    def __init__(self, system, random, stl, stl_utils):
        self.system = system
        self.random = random
        self.stl_utils = stl_utils
        self.stl = stl

        print("render class loaded")

    def mesh1(self, vertices):

        facets = vertices.reshape((-1, 9))
        lines = ["mesh {"]

        fct = "  triangle {{\n    <{1}, {0}, {2}>,\n    <{4}, {3}, {5}>,\n" \
              "    <{7}, {6}, {8}>\n  }}"
        lines += [fct.format(*f) for f in facets]
        lines += ["texture {"]
        lines += ["pigment { color rgb<0.9, 0.9, 0.9> }"]
        lines += ["finish { ambient 0.2 diffuse 0.7 }"]
        lines += ['}']
        lines += ['}']
        return '\n'.join(lines)

    def __stl_to_pov(self , filename, pov_file):
        vertices, name = self.stl.readstl(filename, "utf-8")
        file = open(pov_file, 'w+')
        file.write(self.mesh1(vertices))

        global_setting_file = open("./global_povray_setting.txt", "r")
        file.write(global_setting_file.read())
        file.close()
        global_setting_file.close()




    def render_stl(self, folder_name, filename):

        pov_file = folder_name + "input.pov"
        png_name = "preview.png"
        png_path = folder_name + png_name

        self.__stl_to_pov(folder_name + filename, pov_file)
        render_command = "povray  -i\"" + pov_file + "\" +FN +W1920 +H1080 -o\"" + png_path + "\" +Q9 +AM1 +A +UA"
        self.system(render_command)
        return png_name





