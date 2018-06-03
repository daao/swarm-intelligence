class Reader:
    def __init__(self, file):
        self.matrix_A = []
        self.matrix_B = []
        self.size = 0
        self.read_file(file)

    # Read the instance file and store the different information
    def read_file(self, file):
        f = open(file, "r")

        # define the type of information read
        section = 0
        for line in f.readlines():
            i = 0
            j = 0

            # Read the size of the matrix
            if section == 0:
                # End to read the size of matrix, update section to the next
                if line.strip() == "\n" or line.strip() == "":
                    section += 1
                else:
                    self.size = int(line.strip()) # get the size of the matrix
                    # Initialize the matrices
                    for i in range(self.size):
                        self.matrix_A.append([])
                        self.matrix_B.append([])
            # Read the matrix A and get information
            elif section == 1:
                # End to read the matrix A, update section to the next
                if line.strip() == "\n" or line.strip() == "":
                    section += 1
                    i = 0
                    j = 0
                else:
                    split = line.split(" ") # split the line into array
                    values = [v.strip() for v in split if v.strip() != ""] # filter the array : remove empty cell
                    for val in values:
                        if val != "":
                            self.matrix_A[i].append(int(val)) # store the values in the matrix A
                        i += 1
            # Read the matrix B and get the information
            elif section == 2:
                if line.strip() != "\n" and line.strip() != "":
                    split = line.split(" ") # split the line into array
                    values = [v.strip() for v in split if v.strip() != ""] # filter the array : remove empty cell
                    for val in values:
                        self.matrix_B[i].append(int(val.strip())) # store the values in the matrix B
                        i += 1

