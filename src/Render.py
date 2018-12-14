class Render:

    def __init__(self, system, random, stl, stl_utils, mesh, stl_numpy):
        self.system = system
        self.random = random
        self.stl_utils = stl_utils
        self.stl = stl
        self.mesh = mesh
        self.stl_numpy = stl_numpy

        print("render class loaded")

    def get_world(self, filename):

        stl_object = self.mesh.Mesh.from_file(filename)

        minx = maxx = miny = maxy = minz = maxz = None
        for p in stl_object.points:
            # p contains (x, y, z)
            if minx is None:
                minx = p[self.stl_numpy.Dimension.X]
                maxx = p[self.stl_numpy.Dimension.X]
                miny = p[self.stl_numpy.Dimension.Y]
                maxy = p[self.stl_numpy.Dimension.Y]
                minz = p[self.stl_numpy.Dimension.Z]
                maxz = p[self.stl_numpy.Dimension.Z]
            else:
                maxx = max(p[self.stl_numpy.Dimension.X], maxx)
                minx = min(p[self.stl_numpy.Dimension.X], minx)
                maxy = max(p[self.stl_numpy.Dimension.Y], maxy)
                miny = min(p[self.stl_numpy.Dimension.Y], miny)
                maxz = max(p[self.stl_numpy.Dimension.Z], maxz)
                minz = min(p[self.stl_numpy.Dimension.Z], minz)

        x = maxx - minx
        y = maxy - miny
        z = maxz - minz

        largest_axis = max([x, y, z])
        location_const = str(largest_axis * 1.5)

        look_at_x = str((maxx - minx) / 2 + minx)
        look_at_y = str((maxy - miny) / 2 + miny)
        look_at_z = str((maxz - minz) / 2 + minz)

        light_x = str(maxx * 1.5)
        light_y = str(maxy * 1.5)
        light_z = str(maxz *1.5)


        lines = ["  camera {"]
        lines += ["    location <" + location_const + ", " + location_const + ", " + location_const + ">"]
        lines += ["up z sky z"]
        lines += ["look_at <" + look_at_x + ", " + look_at_y + ", " + look_at_z + ">"]
        lines += ["}"]
        lines += ["  light_source { <" + light_x + ", " + light_y + ", " + light_z + "> color rgb<1, 1, 1> }"]

        return '\n'.join(lines)


    def mesh1(self, vertices):

        facets = vertices.reshape((-1, 9))
        lines = ["mesh {"]

        fct = "  triangle {{\n    <{1}, {0}, {2}>,\n    <{4}, {3}, {5}>,\n" \
              "    <{7}, {6}, {8}>\n  }}"
        lines += [fct.format(*f) for f in facets]
        lines += ["texture {"]
        lines += ["pigment { color rgb<0, 1, 0> }"]
        lines += ["finish { phong 1.0 reflection{0.2} }"]
        lines += ['}']
        lines += ['}']
        return '\n'.join(lines)

    def __stl_to_pov(self , filename, pov_file):
        vertices, name = self.stl.readstl(filename, "utf-8")
        file = open(pov_file, 'w+')
        file.write(self.mesh1(vertices))

        world = self.get_world(filename)
        file.write(world)

        plain_file = open("./plain.pov", "r")
        file.write(plain_file.read())

        file.close()





    def render_stl(self, folder_name, filename):

        pov_file = folder_name + "input.pov"
        png_name = "preview.png"
        png_path = folder_name + png_name

        self.__stl_to_pov(folder_name + filename, pov_file)
        render_command = "povray  -i\"" + pov_file + "\" +FN +W1920 +H1200 -o\"" + png_path + "\" +Q9 +AM1 +A +UA"
        self.system(render_command)
        return png_name





