class Past(object):
    data = [None for i in range(9)]

    def __init__(self, data):
        self.data = data % 512

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self)

    def __cmp__(self, other):
        return cmp(self.data, other.data)

    ### Individual cells in the past. ###
    @property
    def nw(self):
        return 1 if self.data & 256 else 0

    @property
    def n(self):
        return 1 if self.data & 128 else 0

    @property
    def ne(self):
        return 1 if self.data & 64 else 0

    @property
    def w(self):
        return 1 if self.data & 32 else 0

    @property
    def c(self):
        return 1 if self.data & 16 else 0

    @property
    def e(self):
        return 1 if self.data & 8 else 0

    @property
    def sw(self):
        return 1 if self.data & 4 else 0

    @property
    def s(self):
        return 1 if self.data & 2 else 0

    @property
    def se(self):
        return 1 if self.data & 1 else 0

    ### The resulting center cell after a single step. ###
    @property
    def z(self):
        neighbors = sum([self.nw, self.n, self.ne,
                         self.w,          self.e,
                         self.sw, self.s, self.se])
        if self.c:
            if neighbors < 2:
                return 0
            elif neighbors in [2, 3]:
                return 1
            else:
                return 0
        else:
            if neighbors == 3:
                return 1
            else:
                return 0

    ### Transformations for corroboration. ###
    @property
    def NW(self):
        x = [self.nw, self.n,
             self.w,  self.c]
        return vector_to_int(x)

    @property
    def N(self):
        x = [self.nw, self.n, self.ne,
             self.w,  self.c, self.e]
        return vector_to_int(x)

    @property
    def NE(self):
        x = [self.n, self.ne,
             self.c, self.e]
        return vector_to_int(x)

    @property
    def W(self):
        x = [self.nw, self.n,
             self.w,  self.c,
             self.sw, self.s]
        return vector_to_int(x)

    @property
    def E(self):
        x = [self.n, self.ne,
             self.c, self.e,
             self.s, self.se]
        return vector_to_int(x)

    @property
    def SW(self):
        x = [self.w,  self.c,
             self.sw, self.s]
        return vector_to_int(x)

    @property
    def S(self):
        x = [self.w,  self.c, self.e,
             self.sw, self.s, self.se]
        return vector_to_int(x)

    @property
    def SE(self):
        x = [self.c, self.e,
                self.s, self.se]
        return vector_to_int(x)

def vector_to_int(v):
    r = 0
    for i in v:
        r <<= 1
        r += i
    return r

if __name__ == '__main__':
    from random import randint
    p = Past(randint(0, 256))
    print p, '>', p.z
    print p.nw, p.n, p.ne
    print p.w, p.c, p.e
    print p.sw, p.s, p.se
    print
    print 'NW:', p.NW
    print 'N:', p.N
    print 'NE:', p.NE
    print 'W:', p.W
    print 'E:', p.E
    print 'SW:', p.SW
    print 'S:', p.S
    print 'SE:', p.SE
