from ant import Ant
import Params
import numpy as np


class Ants:
    def __init__(self, distances, flows, nb_ants, nb_cities):
        self.distances = np.array(distances).copy()
        self.flows = np.array(flows).copy()
        self.nb_cities = nb_cities
        self.nb_ants = nb_ants
        self.colony = []
        self.pheromone = []
        self.heuristic = []
        for i in range(0, nb_ants):
            self.colony.append(Ant(distances, flows, nb_cities))

    # Find the best cost of the colony
    # @return the index of the ant that have the best solution
    def find_best(self):
        solutions = [x.get_cost() for x in self.colony]
        return solutions.index(min(solutions))

    # Find the worst cost of the colony
    # @return the index of the ant that have the worst solution
    def find_worst(self):
        solutions = [x.get_cost() for x in self.colony]
        return solutions.index(max(solutions))

    # Apply the local search into each ant of the colony
    # Apply the 2-opt algorithm
    def local_search(self):
        for a in self.colony:
            a.search_2_opt()

    # Compute the cost for all ants of the colony
    def compute_all_costs(self):
        for a in self.colony:
            a.compute_cost()

    # Function that initialize the value of the pheromone and the value of heuristic
    def init_pheromone(self, default_value):
        for i in range(0, self.nb_cities):
            self.pheromone.append([])
            self.heuristic.append([])
            for j in range(0, self.nb_cities):
                self.pheromone[i].append(default_value)
                self.heuristic[i].append(self.compute_heuristic(i, j))

    # Compute the heuristic value of a city
    # h(x,y) = 1/d[x,y]*f[x,y] + 1
    def compute_heuristic(self, i, j):
        return 1 /(self.distances[i][j]*self.flows[i][j] + 1)

    # Choose the next city for each ant of the colony
    # The choosing depends on the probabilities of all outgoing path from the current city
    def choose_next_city(self, step):
        for ant in self.colony:
            current_city = ant.get_current_city()
            ant.compute_probabilities(self.pheromone[current_city], self.heuristic[current_city])
            ant.choose_next_neighbour(step)

    # Update the pheromone by following the Rank-Based Ant rules
    def rba_update_pheromone(self):
        self.evaporation()

        for a in self.colony:
            for i in range(self.nb_cities-1):
                j = a.tour[i]
                h = a.tour[i+1]
                delta = self.compute_ranked_ants()
                delta_best = 1/(self.colony[self.find_best()].get_cost())
                self.pheromone[j][h] += delta + Params.singleton.W*delta_best
                self.pheromone[h][j] = self.pheromone[j][h]

    def evaporation(self):
        for i in range(self.nb_cities):
            for j in range(self.nb_cities):
                self.pheromone[i][j] = (1-Params.singleton.RHO)*self.pheromone[i][j]

    # Compute the delta pheromone with the Rank-Based Ant rules
    # Sort the ant from the best to the worst
    # Sum the solution by multiplying each solution by the weight of the rank of the ant
    # More the ant is ranked, more the weight will be big
    def compute_ranked_ants(self):
        solutions = [x.get_cost() for x in self.colony]
        solutions.sort()
        sum = 0
        for r in range(1, Params.singleton.W-1):
            sum += (Params.singleton.W - r)*(1/solutions[r])
        return sum

    # Update the pheromone by following the Elitist Ant System rules
    def eas_update_pheromone(self):
        self.update_pheromone()

        nb_elite = self.count_elite()
        delta = 1 / self.colony[self.find_best()].get_cost()

        for a in self.colony:
            for i in range(self.nb_cities-1):
                j = a.tour[i]
                h = a.tour[i + 1]
                self.pheromone[j][h] += nb_elite * delta
                self.pheromone[h][j] = self.pheromone[j][h]

    # Give the number of ants that have the best solution
    def count_elite(self):
        costs = [x.get_cost() for x in self.colony]
        best = self.colony[self.find_best()].get_cost()
        return costs.count(best)

    # Update the pheromone ine a classic way
    def update_pheromone(self):
        self.evaporation()

        for a in self.colony:
            for i in range(self.nb_cities-1):
                j = a.tour[i]
                h = a.tour[i+1]
                delta = self.delta_pheromone()
                self.pheromone[j][h] += delta
                self.pheromone[h][j] = self.pheromone[j][h]

    # Compute the delta for the updating pheromone
    def delta_pheromone(self):
        sum = 0
        for a in self.colony:
            sum += 1/a.get_cost()
        return sum
