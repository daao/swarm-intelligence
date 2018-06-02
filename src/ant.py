import random as rand
import Params


class Ant:
    def __init__(self, distances, flows, nb_city):
        self.nb_city = nb_city
        self.visited = [False for i in range(nb_city)]
        self.tour = [-1 for i in range(nb_city)]
        self.probabilities = [0 for i in range(nb_city)]
        self.distance = distances
        self.flows = flows
        self.cost = 0
        self.current_city = -1

    # Give the cost of the assignment
    def get_cost(self):
        return self.cost

    # Give the current city of the ant
    def get_current_city(self):
        return self.current_city

    # Place the ant in a city at random
    # @param step : the current step of the computation solution
    def place_ant(self, step):
        start = rand.randrange(self.nb_city)
        self.tour[step] = start
        self.visited[start] = True
        self.current_city = start

    # Select the next city for the assignment depending on the probability of each outgoing path
    # @param step : the current step of the solution's computation
    def choose_next_neighbour(self, step):
        next = self.get_current_city()
        while self.visited[next]:
            cumulative_prob = 0.0
            r = rand.random()
            for i in range(len(self.probabilities)):
                cumulative_prob += self.probabilities[i]
                if r <= cumulative_prob:
                    next = i
                    break
        self.tour[step] = next
        self.visited[next] = True
        self.current_city = next

    # Compute the probability of all possible path since the current city
    # @param pheromone : the values of pheromone of all possible outgoing path since the current city
    # @param heuristic : the values of heuristic of all possible outgoing path since the current city
    def compute_probabilities(self, pheromone, heuristic):
        memory = self.get_memory(pheromone, heuristic)

        for i in range(len(self.probabilities)):
            prob = (pheromone[i]**Params.singleton.ALPHA) * (heuristic[i]**Params.singleton.BETA)
            self.probabilities[i] = prob/memory

    # Compute the memory of the ant in a specific position
    # @param : pheromone, array of double : the values of pheromone of all possible outgoing path in the current city
    # @param : heuristic, array of double : the values of heuristic of all possible outgoing path in the current city
    def get_memory(self, pheromone, heuristic):
        sum = 0
        for i in range(len(pheromone)):
            sum += pheromone[i]**Params.singleton.ALPHA * heuristic[i]**Params.singleton.BETA
        return sum

    # Compute the cost of the assignment
    def compute_cost(self):
        self.cost = 0
        flows_adjust = self.adjust_flows_to_permutation()

        for i in range(self.nb_city):
            for j in range(i,self.nb_city):
                self.cost += self.distance[i][j] * flows_adjust[i][j]

        self.cost *= 2

    # Modify the flow matrix with the value of the assignment
    # Firstly we swap the column each other corresponding to the value of assignment
    # Lastly we swap the line between them corresponding to the value of the assignment
    def adjust_flows_to_permutation(self):
        matrix = []
        for i in range(len(self.tour)):
            matrix.append([])
            for j in range(len(self.tour)):
                city = self.tour[j]
                matrix[i].append(self.flows[i][city])

        new_matrix = []
        for i in range(len(self.tour)):
            city = self.tour[i]
            new_matrix.append(matrix[city])

        return new_matrix

    # Function applies the 2-opt algorithm for the local search
    # Loop over the assignment and swap 2 indices,
    # if the swap produces a better solution, we keep the swap
    # otherwise we revert the permutation
    def search_2_opt(self):
        for i in range(len(self.tour)):
            idx_perm = rand.choice([j for j in range(len(self.tour)-1) if j != i])
            self.compute_cost()
            current_cost = self.get_cost()

            tmp_val = self.tour[i]
            self.tour[i] = self.tour[idx_perm]
            self.tour[idx_perm] = tmp_val

            # If the new solutions is not better than the current, we revert the modification
            self.compute_cost()
            new_cost = self.get_cost()
            if new_cost > current_cost:
                self.tour[idx_perm] = self.tour[i]
                self.tour[i] = tmp_val
                self.cost = current_cost
            # else we continue with the new permutation
