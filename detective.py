from alibi import Alibi

class Detective(object):
    width = 0
    height = 0
    alibis = None
    CONFIDENCE = 0

    def __init__(self, life):
        self.width = life.width
        self.height = life.height
        self.alibis = [[Alibi()
                        for c in range(self.width)]
                       for r in range(self.height)]

        # Filter for present state
        for r in range(self.height):
            for c in range(self.width):
                self.alibis[r][c].filter('z', life.state_at(r, c))

        for r in range(self.height):
            # Left edge
            for direction in ['nw', 'w', 'sw']:
                self.alibis[r][0].filter(direction, 0)

            # Right edge
            for direction in ['ne', 'e', 'se']:
                self.alibis[r][self.c_].filter(direction, 0)

        for c in range(self.width):
            # Top edge
            for direction in ['nw', 'n', 'ne']:
                self.alibis[0][c].filter(direction, 0)

            # Bottom edge
            for direction in ['sw', 's', 'se']:
                self.alibis[self.r_][c].filter(direction, 0)

        # Remove all the impossible alibis.
        self.interrogate()

    def __str__(self):
        return '\n'.join(['  '.join(['%0.2f' % alibi.confidence
                                     for alibi in row]) for row in self.alibis])

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for row in self.alibis:
            for alibi in row:
                yield alibi

    @property
    def r_(self):
        return self.height - 1

    @property
    def c_(self):
        return self.width - 1

    def __dict__(self):
        return {'width': self.width,
                'height': self.height,
                'cells': [a.confidence for row in self.alibis for a in row]
               }

    def alibi_at(self, row, column):
        if row < 0 or row >= self.height:
            return None
        if column < 0 or column >= self.width:
            return None
        return self.alibis[row][column]

    def neighbors_of(self, r, c):
        N = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
             (r, c - 1),                 (r, c + 1),
             (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
        return [self.alibi_at(r, c) for (r, c) in N]

    def interrogate(self):
        # Corroborate between aliases. Return number of aliases removed.
        removed = 1
        while removed > 0:
            removed = 0
            for r in range(self.height):
                for c in range(self.width):
                    neighbors = self.neighbors_of(r, c)
                    suspect = self.alibi_at(r, c)
                    removed += suspect.corroborate(neighbors)

    def guess(self, confidence=0.5):
        # Any alibis with greater than 75% or less than 25%, we'll guess at.
        removed = 1
        while removed > 0:
            removed = 0
            self.interrogate()
            for r in range(self.height):
                for c in range(self.width):
                    suspect = self.alibi_at(r, c)
                    filtered = 0
                    if len(suspect) <= 1:
                        continue
                    conf = suspect.confidence
                    if conf in [0.0, 1.0]:
                        continue
                    if conf <= confidence:
                        # Most likely dead
                        filtered = suspect.filter('c', 0)
                        removed += filtered
                    elif conf >= 1 - confidence:
                        # Most likely alive
                        filtered = suspect.filter('c', 1)
                        removed += filtered
                    if filtered:
                        self.interrogate()

    @property
    def span(self):
        return reduce(lambda x, y: x * y, [a.span for a in self])
