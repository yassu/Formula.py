class MathItem:
    def __init__(self, data):
        self._data = data
        self._before = None
        self._afters = []

    @property
    def before(self):
        return self._before

    @property
    def data(self):
        return self._data

    def _set_before(self, before):
        self._before = before

    def append(self, item):
        self._afters.append(item)
        item._set_before(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._data == other._data

    def __getitem__(self, ind):
        return self._afters[0]

    def __ne__(self, other):
        return not (self == other)
