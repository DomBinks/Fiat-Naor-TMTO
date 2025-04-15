import random
from abc import abstractmethod

class TMTO:

    def __init__(self, f, N, t, m, l, log):
        """Default constructor for a TMTO"""

        self._f = f
        self._f_calls = 0

        self._N = N
        self._t = t
        self._m = m
        self._l = l

        self._log = log

    def log(self, msg):
        """Log the message if logging is enabled"""

        if self._log:
            print(msg)

    def _rand_N(self):
        """Generate a random number in {1,...,N}"""

        return random.randint(1, self._N)

    def _f_count(self, x):
        """Calls the function and updates the calls count"""

        self._f_calls += 1
        return self._f(x)

    def get_f_calls(self):
        """Get the number of function calls made by this TMTO"""

        return self._f_calls

    def success_rate(self, N):
        """Get the success rate of the TMTO with N size preimages, alongside metadata"""

        self.log("Calculating success rate...")

        samples = 500
        #samples = 65536

        success = 0
        collisions = 0
        alarms = 0
        a_found = 0
        t_found = 0
        for i in range(samples):
            inp = random.randint(1, N)
            #inp = i + 1

            (p, metadata) = self.find_preimage(self._f(inp))
            if p:
                success += 1
                if metadata["tmto"] == "fiat-naor": # Fiat-Naor TMTO
                    if metadata["a"]:
                        a_found += 1
                    else:
                        t_found += 1
                else: # Rainbow tables
                    if p != inp:
                        collisions += 1
                    alarms += metadata["alarms"]

        if metadata["tmto"] == "fiat-naor": # Fiat-Naor TMTO
            if a_found == 0 and t_found == 0:
                return success / samples, {"a_found": 0.0, "t_found": 0.0}
            else:
                return success / samples, {"a_found": a_found / (a_found + t_found), "t_found": t_found / (a_found + t_found)}
        else: # Rainbow Tables
            return success / samples, {"collisions": collisions / samples, "alarms": alarms}

    @abstractmethod
    def find_preimage(self, image):
        """Find the preimage of the given image, alongside metadata"""
        pass