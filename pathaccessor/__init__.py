from collections import Mapping, Sequence


class PathAccessorBase (object):
    def __init__(self, value, path):
        assert isinstance(path, str), (value, path)
        self._value = value
        self._path = path
        self._mappingaccessor = type(self)

    def __repr__(self):
        return '<{0.__name__} {1._path} {1._value!r}>'.format(type(self), self)

    # A private utility method for subclasses:
    def _get(self, key, exctype, pathfmt):
        v = self._value
        try:
            thing = v[key]
        except (KeyError, IndexError, AttributeError):
            raise exctype('{!r} has no member {!r}'.format(self, key))

        return wrap(
            thing,
            pathfmt.format(self._path, key),
            mappingaccessor=self._mappingaccessor,
        )


class PathAccessorKeyError (KeyError):
    def __str__(self):
        return self.args[0]


class MappingPathAccessor (PathAccessorBase, Mapping):
    def __init__(self, d, path):
        assert isinstance(d, Mapping), (d, path)
        PathAccessorBase.__init__(self, d, path)

    def __getitem__(self, key):
        return self._get(key, PathAccessorKeyError, '{}[{!r}]')

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)


class MappedAttrPathAccessor (MappingPathAccessor):
    def __getattr__(self, key):
        return self._get(key, AttributeError, '{}.{}')


class SequencePathAccessor (PathAccessorBase, Sequence):
    def __init__(self, s, path, mappingaccessor=MappingPathAccessor):
        assert isinstance(s, Sequence), (s, path)
        PathAccessorBase.__init__(self, s, path)
        self._mappingaccessor = mappingaccessor

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._get(key, IndexError, '{}[{!r}]')
        else:
            raise TypeError(
                'Index {!r} of {!r} not an integer'.format(
                    key,
                    self,
                ),
            )

    def __len__(self):
        return len(self._d)


def wrap(thing, path, mappingaccessor=MappingPathAccessor):
    if isinstance(thing, Mapping):
        return mappingaccessor(thing, path)
    elif isinstance(thing, Sequence):
        return SequencePathAccessor(thing, path, mappingaccessor)
    else:
        return thing
