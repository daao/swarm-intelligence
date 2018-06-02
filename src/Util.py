import Params


# Read the configurations to get the list of configuration for the Automatic Configuration
def read_configuration_files():
    configurations = []
    f = open("../configurations.txt", "r")

    for line in f.readlines():
        split = line.strip().split()
        configurations.append([int(split[0]), int(split[1]), int(split[2]), float(split[3]), int(split[4])])

    return configurations


# Read the configuration file created by the tuning_parameter
# Read depending on the algorithm
def get_configuration():
    if Params.singleton.eas_flag:
        f = open("../QAP_configurations/eas_config.txt", "r")
    elif Params.singleton.rba_flag:
        f = open("../QAP_configurations/rba_config.txt", "r")

    line = f.readline() # read the configuration line
    f.close()
    split = line.split() # [NN_ANTS, ALPHA, BETA, RHO, OMEGA]
    Params.singleton.set_nb_ant(int(split[0])) # set the number of ants
    Params.singleton.set_alpha(float(split[1])) # set alpha
    Params.singleton.set_beta(float(split[2])) # set beta
    Params.singleton.set_rho(float(split[3])) # set rho
    Params.singleton.set_omega(int(split[4])) # set omega


# Set the arguments received in command line to the parameters
def set_parameters(argv):
    if "-a" in argv or "--alpha" in argv:
        index = argv.index("-a") if "-a" in argv else argv.index("--alpha")
        Params.singleton.set_alpha(argv[index])

    if "-b" in argv or "--beta" in argv:
        index = argv.index("-b") if "-b" in argv else argv.index("--beta")
        Params.singleton.set_beta(argv[index])

    if "-rh" in argv or "--rho" in argv:
        index = argv.index("-rh") if "-rh" in argv else argv.index("--rho")
        Params.singleton.set_rho(argv[index])

    if "-e" in argv or "--eas" in argv:
        Params.singleton.set_eas_flag(True)
    elif "-r" in argv or "--rba" in argv:
        Params.singleton.set_rba_flag(True)

    if "-l" in argv or "--lcs" in argv:
        Params.singleton.set_lcs_flag(True)

    if "--ants" in argv:
        index = argv.index("--ants")
        Params.singleton.set_nb_ant(int(argv[index + 1]))

    if "--time" in argv:
        index = argv.index("--time")
        Params.singleton.set_time(int(argv[index + 1]))

    if "-nr" in argv or "--runs" in argv:
        index = argv.index("-nr") if "-nr" in argv else argv.index("--runs")
        Params.singleton.set_max_runs(int(argv[index+1]))

    if "-t" in argv or "--trials" in argv:
        index = argv.index("-nt") if "-nt" in argv else argv.index("--trials")
        Params.singleton.set_max_tries(int(argv[index + 1]))

    if "-o" in argv or "--omega" in argv:
        index = argv.index("-o") if "-o" in argv else argv.index("--omega")
        Params.singleton.set_omega(int(argv[index + 1]))

    if "-opt" in argv or "--optimal" in argv:
        index = argv.index("-opt") if "-opt" in argv else argv.index("--optimal")
        Params.singleton.set_optimal(int(argv[index+1]))

    if "-op" in argv or "--optimum" in argv:
        index = argv.index("-op") if "op" in argv else argv.index("--optimum")
        f = open(argv[index+1], "r")
        for opt in f.readlines():
            if opt.strip() != "" or opt.strip() != "\n":
                Params.singleton.add_optimum(int(opt.strip()))
