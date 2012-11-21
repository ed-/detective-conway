class Cell(object):
    _current = None
    _next = None
    _row = None
    _column = None

    def __init__(self, state=0):
        self._current = state

    @property
    def state(self):
        return self._current

    def prep(self, state):
        self._next = state

    def tick(self):
        if self._next is not None:
            self._current = self._next
            self._next = None
