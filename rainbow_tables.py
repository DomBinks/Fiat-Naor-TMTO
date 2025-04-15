from tmto import *

class RainbowTables(TMTO):
    """Rainbow Tables class"""

    def __init__(self, f, N, t, m, l, log=False):
        """Constructor for Rainbow Tables"""

        super().__init__(f, N, t, m, l, log)
        self._tables = [{}] * (self._l+1)

        self._generate_tables()

    def _r(self, y, i, k):
        """Reduction function"""

        return (y + (i*self._t) + k) % self._N

    def _generate_tables(self):
        """Generate rainbow tables"""

        self.log("Generating tables")

        for i in range(1, self._l+1):
            for j in range(1, self._m+1):
                sp = self._rand_N()
                ep = sp

                for k in range(self._t):
                    ep = self._r(self._f(ep), i, k)

                if ep not in self._tables[i].keys():
                    self._tables[i][ep] = sp

    def find_preimage(self, image):
        """Find the preimage of the given image, alongside metadata"""

        self.log("Finding preimage of " + str(image))

        alarms = 0

        for s in range(self._t-1, -1, -1):
            for i in range(1, self._l+1):
                op = self._r(image, i, s)

                for k in range(s+1, self._t):
                    op = self._r(self._f_count(op), i, k)
                
                if op in self._tables[i].keys():
                    tp = self._tables[i][op]

                    for k in range(0, s):
                        tp = self._r(self._f_count(tp), i, k)
                    
                    if self._f_count(tp) == image:
                        self.log("Found preimage")
                        return tp, {"tmto": "rainbow-tables", "alarms" : alarms}
                    else:
                        alarms += 1

        self.log("Preimage not found")
        return None, {"tmto": "rainbow-tables"}