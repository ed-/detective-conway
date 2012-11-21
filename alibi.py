from past import Past

class Alibi(object):
    pasts = []
    directions = ['nw', 'n', 'ne',
                  'w',  'c', 'e',
                  'sw', 's', 'se']

    def __init__(self):
        self.pasts = [Past(i) for i in range(512)]

    def __str__(self):
        x = self.cloud
        values = [x[d] for d in self.directions]
        return ", ".join(['%0.3f' % v for v in values])

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for p in self.pasts:
            yield p

    def __len__(self):
        return len(self.pasts)

    @property
    def cloud(self):
        # compound the histories into a single probability grid
        aggregate = {}
        for past in self.pasts:
            for d in self.directions:
                aggregate[d] = (aggregate.get(d, 0) + getattr(past, d))
        for d in self.directions:
            aggregate[d] = float(aggregate[d]) / len(self.pasts)
        return aggregate

    @property
    def confidence(self):
        # Confidence that a cell was alive before
        assert len(self.pasts) > 0
        return float(self.cloud['c'])
    
    @property
    def span(self):
        if self.confidence in [0.0, 1.0]:
            return 1
        return len(self.pasts)

    def filter(self, direction, state):
        old_pasts = len(self.pasts)
        self.pasts = [p for p in self.pasts
                      if getattr(p, direction) == state]
        removed = old_pasts - len(self.pasts)
        return removed

    def corroborate(self, others):
        old_pasts = len(self.pasts)
        [nw_n, n_n, ne_n, w_n, e_n, sw_n, s_n, se_n] = others
        directions = [
            (nw_n, 'NW', 'SE'),
            (n_n, 'N', 'S'),
            (ne_n, 'NE', 'SW'),
            (w_n, 'W', 'E'),
            (e_n, 'E', 'W'),
            (sw_n, 'SW', 'NE'),
            (s_n, 'S', 'N'),
            (se_n, 'SE', 'NW')]

        for (neighbor, direction, opposite) in directions:
            if neighbor is not None:
                neighbor = set([getattr(a, opposite) for a in neighbor])
                self.pasts = [p for p in self.pasts
                              if getattr(p, direction) in neighbor]

        removed = old_pasts - len(self.pasts)
        return removed
