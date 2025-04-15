import math
from tmto import *
from hash_functions import *

class FiatNaor(TMTO):
    """Fiat-Naor TMTO class"""

    def __init__(self, f, N, t, m, l, d, log=False):
        """Constructor for Fiat-Naor TMTO"""

        super().__init__(f, N, t, m, l, log)
        self._S = self._m * self._l
        self._d = d
        self._k = math.ceil(self._t * math.log2(self._N))
        self._gs = [[None] * (self._l+1)] * (self._d+1)
        self._A = [{}] * (self._d+1)
        self._T = [[{}] * (self._l+1)] * (self._d+1)

        self._generate_gs()
        self._generate_A()
        self._generate_T()
        self._f_calls = 0 # Reset f count before finding preimages

    def _h_i(self, i, d, x):
        """Perform h_i"""

        inp = self._gs[d][i](self._f_count(x))
        j = 1

        while (self._f_count(inp) in self._A[d].keys()) and j <= (self._k/2):
            inp = self._gs[d][i](inp)
            j += 1

        if j <= (self._k/2):
            return inp
        else:
            return None

    def _t_h_i(self, t, i, d, x):
        """Compute t iterations of h_i"""

        h_i_t_x = x
        for _ in range(t):
            h_i_t_x = self._h_i(i, d, h_i_t_x)
            if not h_i_t_x:
                return None

        return h_i_t_x

    def _j_g_i(self, i, d, y):
        """Compute the jth iteration of g_i, returning None if undefined"""

        inp = self._gs[d][i](y)
        j = 1

        while (self._f_count(inp) in self._A[d].keys()) and (j < (self._k / 2)):
            inp = self._gs[d][i](inp)
            j += 1

        if j < (self._k / 2):
            return inp
        else:
            return None

    def _generate_gs(self):
        """Generate the k-wise independent functions"""

        self.log("Generating gs...")

        for d in range(1, self._d+1):
            self._gs[d] = [lambda x: mmh3_N(x + i + d*self._l, self._N) for i in range(1, self._l + 1)]
            self._gs[d] = [None] + self._gs[d]

    def _generate_A(self):
        """Generate the A Table"""

        self.log("Generating A...")

        for d in range(1, self._d+1):
            for _ in range(self._S):
                x_i = self._rand_N()
                if x_i not in self._A[d].keys():
                    self._A[d][x_i] = self._f(x_i)

    def _generate_T(self):
        """Generate the T table"""

        self.log("Generating T...")

        for d in range(1, self._d+1):
            for i in range(1, self._l+1):
                for _ in range(self._m):
                    x = self._rand_N()
                    h_i_t_x = self._t_h_i(self._t, i, d, x)
                    if h_i_t_x and (h_i_t_x not in self._T[d][i].keys()):
                        self._T[d][i][h_i_t_x] = x

    def find_preimage(self, image):
        """Find the preimage of the given image, alongside metadata"""

        self.log("Finding preimage of " + str(image))

        for d in range(1, self._d+1):
            if image in self._A[d].values():
                for (x, fx) in self._A[d].items():
                    if fx == image:
                        self.log("Found preimage in A")
                        return x, {"tmto": "fiat-naor", "a" : True, "t" : False}

            for i in range(1, self._l+1):
                u_i = self._j_g_i(i, d, image)
                if not u_i:
                    continue

                for p in range(1, self._t+1):
                    if u_i in self._T[d][i].keys():
                        z = self._t_h_i(self._t-p, i, d, self._T[d][i][u_i])

                        if self._f_count(z) == image:
                            self.log("Found preimage in T")
                            return z, {"tmto": "fiat-naor", "a" : False, "t" : True}

                    u_i = self._h_i(i, d, u_i)
                    if not u_i:
                        break

        self.log("Preimage not found")
        return None, {"tmto": "fiat-naor"}