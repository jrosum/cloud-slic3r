class RepairStl:

    def __init__(self, system):
        self.system = system

    def repair_and_save_ascii(self, folder_name, file_name):
        return self.system("cd " + folder_name + " && admesh --nearby --iterations=100 --normal-directions --write-ascii-stl=" + file_name + " " + file_name)



