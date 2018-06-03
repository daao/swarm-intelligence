import Params
import Util
from reader import Reader
from ants import Ants
import os
import sys
import numpy as np
import time

tries = []
solution = sys.maxsize


# Function that reset the tour of each ant,
# place each ant at a random city
# build the assignment by choosing the next city according to the probabilities
# and compute the cost of each ant
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


# Update the pheromone trail of the colony depending on the system
def update_pheromone(ants):
    if Params.singleton.eas_flag:
        ants.eas_update_pheromone()
    elif Params.singleton.rba_flag:
        ants.rba_update_pheromone()


# Check the terminal condition of the algorithm
def terminal_condition(run, start):
    return ((run >= Params.singleton.MAX_RUN and interval(start) >= Params
           .singleton.time) or (runs[run] <= Params.singleton.optimal))


# Compute the time elapsed between the start of trial and now
def interval(start):
    return time.time() - start


# save each run of the system
def save_run(run, ants):
    best_index_ant = ants.find_best() # give the index of the best ant
    best_cost = ants.colony[best_index_ant].get_cost() # get the best solution
    runs[run] = best_cost # store the best


# Get all best solution for each run
# Select the best one and store it
def save_best_run():
    run_solutions = [x for x in runs] # Get the best solution for each run
    index_best_run = run_solutions.index(min(run_solutions)) # Get the index of the best
    tries.append(runs[index_best_run]) # Store the best run tuple


# Get all best cost for each try
# Select the best one
# Store it
def get_best_solution_on_instance():
    try_solutions = [x for x in tries] # Get the best solution for each try
    index_best_try = try_solutions.index(min(try_solutions)) # Get the index of the best try
    global solution
    solution = tries[index_best_try] # set the solution


# Print the best solution of a run
def exit_run(run, ants):
    print("----- RESULTS RUN " + str(run + 1) + " -----")
    print("Best solution : " + str(ants.colony[ants.find_best()].get_cost()))


# Print the statistic of a trial
def exit_trial(trial):
    print("----- RESULTS TRIAL " + str(trial + 1) + " -----")
    print("Best solution : " + str(min(runs)))
    print("Worst solution : " + str(max(runs)))
    print("Mean : " + str(np.mean(runs)))
    print("Standard deviation : " + str(np.std(runs)))


Util.set_parameters(sys.argv) # set all parameters and value from arguments command

# get the instance for the run
index_instance = sys.argv.index("-i") if "-i" in sys.argv else sys.argv.index("--instance")
path = sys.argv[index_instance+1]
filename = os.path.basename(path)

qap = Reader(path) # construct the problem

Util.get_configuration() # get the best configuration of the ant system
runs = [sys.maxsize for i in range(Params.singleton.MAX_RUN)]

for t in range(Params.singleton.MAX_TRY):
    colony = Ants(qap.matrix_A, qap.matrix_B, Params.singleton.nb_ants, qap.size)
    colony.init_pheromone(1 / (Params.singleton.RHO * qap.size))

    run = 0
    start = time.time()
    while not terminal_condition(run, start):
        construct_solutions(colony) # build the solution for each ant

        if Params.singleton.lcs_flag:
            colony.local_search() # apply the local search

        update_pheromone(colony) # update the pheromone depending on the ant system

        save_run(run, colony) # Save the current run

        exit_run(run, colony) # Print the information about the run
        run += 1
    save_best_run() # Save the the run that have the best results
    exit_trial(t) # Print the statistic about the trial
    runs = [sys.maxsize for i in range(Params.singleton.MAX_RUN)]
get_best_solution_on_instance() # Retrieve the best try of the instance
tries.clear()
