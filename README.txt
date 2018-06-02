!IMPORTANT!
For running the project on Linux, you need to be in the folder "src" to run the code.

1. Scripts 
For the project, there is different executable script :

1.2 Automatic tuning configuration ---
tuning_parameter.py : program that compute the best configuration based on a Iterative Algorithm Configuration

ARGUMENTS
-e, --eas : enable the Elitist Ant System
-r, --rba : enable Rank-Based Ant System

-o, --omega <value_omega> : set the value of OMEGA (used for RBA)
-nr, --runs <number_runs> :  number of steps in each trial (default : 10)
-nt, --trials <number_try> : number of independent trials (runs) (default : 1)
-op, --optimum <file_optimum> : set the optimal solution for each instance (read details later)

If you want to run the "tuning_parameter", you need to know that the program will test the selected algorithm regarding
a list of predefined configuration. You can see the list in the file "configurations.txt".
If you want to customize the list, you just need to respect the following format :

[NB_ANTS] [ALPHA] [BETA] [RHO] [OMEGA]

which each line correspond to one configuration.
The pogram will test each one and retrieve in the folder "QAP_configurations" the best configuration found.
[IMPORTANT] The technique is not the best one so you can have different best configuration if you run the
program multiple times.

If you provide the optimum file, you need to define the optimal solution for each instance of "QAP_instances" where each
line is the optimal solution. (!ORDER!) The first line will be the optimal solution for the first instance, and so on.

1.3 ACO ---
aco.py : program that will execute the ant system on all instances and return the results (one file per algorithm)

ARGUMENTS :
-e, --eas : enable mode EAS
-r, --rba : enable mode RBA
-l, --lcs : enable the local search algorithm (2-opt)

-a, --alpha : set the value of alpha*
-b, --beta : set the value of beta *
-rh, --rho : set the value of rho*
--ants : set the number of ants*
-o, --omega <value_omega>*

-nr, --runs <nb_runs> : number of steps in each trial (default : 10)
-nt, --trials <number_try> : number of independent trials (runs) (default : 1)
-opt, --optimal <value> : to stop if tour better or equal optimum is found
-i, --instance <instance_test> : get the instance file test

The program will give in the stdout the best solution for each run and the best result and statistics for each trial.

* : if you don't define those argument, the program will get the best configuration of the algorithm in the folder "QAP_configurations"

2. FOLDERS -----
data : contains data used to create the different plots for the report
QAP_configurations : contains output file from the script "tuning_parameter", 1 file per algorithm that remains the best configuration
QAP_instances : contains instances for the ACO
results : contains the 2 csv files. Those files are the results for the each algorithm
src : contains the code and scripts for the project
