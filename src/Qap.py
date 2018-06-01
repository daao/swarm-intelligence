class Qap:
    def __init__(self, file):
        self.matrix_A = []
        self.matrix_B = []
        self.size = 0
        self.read_file(file)

    def read_file(self, file):
        f = open(file, "r")

        section = 0
        for line in f.readlines():
            i = 0
            j = 0
            if section == 0:
                if line.strip() == "\n" or line.strip() == "":
                    section += 1
                else:
                    self.size = int(line.strip())
                    for i in range(self.size):
                        self.matrix_A.append([])
                        self.matrix_B.append([])
            elif section == 1:
                if line.strip() == "\n" or line.strip() == "":
                    section += 1
                    i = 0
                    j = 0
                else:
                    split = line.split(" ")
                    values = [v.strip() for v in split if v.strip() != ""]
                    for val in values:
                        if val != "":
                            self.matrix_A[i].append(int(val))
                        i += 1
            elif section == 2:
                if line.strip() != "\n" and line.strip() != "":
                    split = line.split(" ")
                    values = [v.strip() for v in split if v.strip() != ""]
                    for val in values:
                        self.matrix_B[i].append(int(val.strip()))
                        i += 1

