import unittest
import re
from pathaccessor.impl import (
    MappingPathAccessor,
    MappedAttrsPathAccessor,
    PathAccessorBase,
    SequencePathAccessor,
)


class PathAccessorBaseTests (unittest.TestCase):
    TargetClass = PathAccessorBase
    TargetValue = {'a': 'aardvark'}

    def assertRaisesLiteral(self, exc, msg, f, *args, **kw):
        self.assertRaisesRegexp(
            exc,
            '^{}$'.format(re.escape(msg)),
            f,
            *args,
            **kw
        )

    def test_len(self):
        pab = self.TargetClass(self.TargetValue, 'ROOT')
        self.assertEqual(len(self.TargetValue), len(pab))

    def test_repr(self):
        pab = self.TargetClass(self.TargetValue, 'ROOT')
        expected = "<{} ROOT {}>".format(
            self.TargetClass.__name__,
            repr(self.TargetValue),
        )
        actual = repr(pab)
        self.assertEqual(expected, actual)


class MappingPathAccessorTests (PathAccessorBaseTests):
    TargetClass = MappingPathAccessor

    def test_keyerror(self):
        mpa = MappingPathAccessor({}, 'ROOT')
        self.assertRaisesLiteral(
            KeyError,
            '<MappingPathAccessor ROOT {}> has no member 42',
            mpa.__getitem__,
            42,
        )

    def test_keys(self):
        mpa = MappingPathAccessor(
            {
                'weapon': 'sword',
                'armor': 'leather'
            },
            'ROOT',
        )
        self.assertEqual({'weapon', 'armor'}, set(mpa.keys()))


class MappedAttrsPathAccessorTests (PathAccessorBaseTests):
    TargetClass = MappedAttrsPathAccessor

    def setUp(self):
        self.mapa = MappedAttrsPathAccessor(
            {'foo': 'bar', 'get': 'got'},
            'THINGY',
        )

    def test_attribute_access_versus_getitem(self):
        self.assertEqual('bar', self.mapa.foo)
        self.assertEqual('bar', self.mapa['foo'])

    def test_tricky_attribute_access(self):
        thing1 = self.mapa.get
        thing2 = self.mapa['get']
        self.assertEqual('got', thing1)
        self.assertEqual(thing1, thing2)

        # If you need a Mapping interface use this API:
        mpa = MappingPathAccessor.fromMappedAttrs(self.mapa)
        self.assertEqual('bar', mpa.get('foo'))
        self.assertEqual('got', mpa.get('get'))
        self.assertEqual('banana', mpa.get('fruit', 'banana'))


class CompoundStructureTests (PathAccessorBaseTests):
    def setUp(self):
        self.structure = {'a': [{"foo": [None, [], 1337]}]}

    def test_mapping_access_success(self):
        mpa = MappingPathAccessor(self.structure, 'ROOT')
        elem = mpa['a'][0]['foo'][2]
        self.assertEqual(1337, elem)

    def test_mappedattrs_access_success(self):
        mpa = MappedAttrsPathAccessor(self.structure, 'ROOT')
        elem = mpa.a[0].foo[2]
        self.assertEqual(1337, elem)

    def test_mapping_access_error(self):
        mpa = MappingPathAccessor(self.structure, 'ROOT')
        child = mpa['a'][0]['foo'][1]
        self.assertRaisesLiteral(
            TypeError,
            ("Index 'bananas' of "
             + "<SequencePathAccessor ROOT['a'][0]['foo'][1] []>"
             + " not an integer"),
            child.__getitem__,
            'bananas',
        )

    def test_mappedattrs_access_error(self):
        mapa = MappedAttrsPathAccessor(self.structure, 'ROOT')
        child = mapa['a'][0].foo[1]
        self.assertRaisesLiteral(
            TypeError,
            ("Index 'bananas' of "
             + "<SequencePathAccessor ROOT['a'][0].foo[1] []>"
             + " not an integer"),
            child.__getitem__,
            'bananas',
        )


class SequencePathAccessorTests (PathAccessorBaseTests):
    TargetClass = SequencePathAccessor
    TargetValue = ['a', 'b', 'c']
