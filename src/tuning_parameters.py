import Params
from reader import Reader
from ants import Ants
import Util
import os
import sys


tries = []
bests_run = []
best_configurations = []


def construct_solutions(ants):

    for a in ants.colony:
        for i in range(len(a.visited)):
            a.visited[i] = False

    step = 0
    for a in ants.colony:
        a.place_ant(step)

    while step < (ants.nb_cities - 1):
        step += 1
        ants.choose_next_city(step)

    ants.compute_all_costs()


def update_pheromone(ants):
    if Params.singleton.eas_flag:
        ants.eas_update_pheromone()
    elif Params.singleton.rba_flag:
        ants.rba_update_pheromone()


def add_run(ants, run):
    runs[run] = (ants.colony[ants.find_best()].get_cost())


def save_best_run():
    index = runs.index(min(runs))
    tries.append(runs[index])


def find_best_tries():
    best_run = tries.index(min(tries))
    bests_run.append(tries[best_run])


def find_best_configurations():
    return bests_run.index(min(bests_run))


def write_configuration(configuration, algo):
    f = open("../QAP_configurations/" + algo + "_config.txt", "w")
    f.write(str(configuration[0]) + " ")
    f.write(str(configuration[1]) + " ")
    f.write(str(configuration[2]) + " ")
    f.write(str(configuration[3]) + " ")
    f.write(str(configuration[4]))
    f.close()


def terminal_condition(run, instance):
    return (run >= Params.singleton.MAX_RUN) or (runs[run] <= Params.singleton.optimums[instance])


path = "../QAP_instances/"
Util.set_parameters(sys.argv)

runs = [sys.maxsize for i in range(Params.singleton.MAX_RUN)]
if len(Params.singleton.optimums) == 0:
    Params.singleton.set_optimums([1 for i in range(len(os.listdir(path)))])

as_algo = "eas" if(Params.singleton.eas_flag) else "rba"

# Retrieve all configurations from the file
seeds = Util.read_configuration_files()

i = 0
for filename in os.listdir(path):
    qap = Reader(path + "" + filename)

    # Loop over each configurations
    for s in range(len(seeds)):
        Params.singleton.set_nb_ant(seeds[s][0])
        Params.singleton.set_alpha(seeds[s][1])
        Params.singleton.set_beta(seeds[s][2])
        Params.singleton.set_rho(seeds[s][3])
        Params.singleton.set_omega(seeds[s][4])

        # Try 3 times each configuration on each instance
        for t in range(Params.singleton.MAX_TRY):
            colony = Ants(qap.matrix_A, qap.matrix_B, Params.singleton.nb_ants, qap.size)
            colony.init_pheromone(1 / ((Params.singleton.RHO) * qap.size))

            run = 0
            while not terminal_condition(run, i):
                print("[DEBUG] Run n°" + str(run+1) + " on configuration n°" + str(s+1))
                print("[DEBUG] Build solutions....")
                construct_solutions(colony)

                print("[DEBUG] Update pheromones")
                update_pheromone(colony)

                print("[DEBUG] Update statistics")
                add_run(colony, run)
                run += 1

            save_best_run() # Save the best run
            runs = [sys.maxsize for i in range(Params.singleton.MAX_RUN)]

        find_best_tries() # Save the best try regarding on the solution
        tries = [] # reset the tries

    best_configurations.append(find_best_configurations()) # Save the best configuration on the instance
    bests_run = [] # reset
    i += 1

configuration = max(set(best_configurations), key=best_configurations.count)
write_configuration(seeds[configuration], as_algo)
print("Best configuration found for " + as_algo + " : " + str(seeds[configuration]))
