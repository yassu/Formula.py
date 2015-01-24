class MathItem(object):
    def __init__(self, data):
        self._data = data
        self._before = None
        self._afters = []

    @property
    def data(self):
        return self._data

    @property
    def before(self):
        return self._before

    def _set_before(self, before):
        self._before = before

    def append(self, after):
        self._afters.append(after)
        after._set_before(self)

    def __getitem__(self, ind):
        return self._afters[ind]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.data == other.data
