import sys


class Params:
    def __init__(self):
        self.ALPHA = 1
        self.BETA = 1
        self.RHO = 0.5
        self.W = 4

        self.nb_ants = 5
        self.MAX_RUN = 10
        self.MAX_TRY = 1

        self.eas_flag = False
        self.rba_flag = False
        self.lcs_flag = False

        self.optimal = 1
        self.optimums = []
        self.time = 0

    def set_alpha(self, alpha):
        self.ALPHA = alpha

    def set_beta(self, beta):
        self.BETA = beta

    def set_rho(self, rho):
        self.RHO = rho

    def set_omega(self, omega):
        self.W = omega

    def set_nb_ant(self, nb_ant):
        self.nb_ants = nb_ant

    def set_max_runs(self, max_run):
        self.MAX_RUN = max_run

    def set_max_tries(self, max_try):
        self.MAX_TRY = max_try

    def set_eas_flag(self, eas_flag):
        self.eas_flag = eas_flag

    def set_rba_flag(self, rba_flag):
        self.rba_flag = rba_flag

    def set_lcs_flag(self, lcs_flag):
        self.lcs_flag = lcs_flag

    def set_optimal(self, optimal):
        self.optimal = optimal

    def set_optimums(self, optimums):
        self.optimums = optimums

    def add_optimums(self, optimum):
        self.optimums.append(optimum)

    def set_time(self, time):
        self.time = time

singleton = Params()