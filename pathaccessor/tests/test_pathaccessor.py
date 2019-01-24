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


class MPABaseMixin (object):
    def setUp(self):
        self.pa = self.TargetClass(
            {
                'weapon': 'sword',
                'armor': 'leather',
                'get': 'got',  # Important case for MappedAttrs
            },
            'ROOT',
        )

    def test_getitem(self):
        self.assertEqual('sword', self.pa['weapon'])

    def test_getitem_keyerror(self):
        self.assertRaisesRegexp(
            KeyError,
            r"^<[A-Za-z]+PathAccessor ROOT {.*}> has no member 42$",
            self.pa.__getitem__,
            42,
        )

    def test_setitem(self):
        self.pa['pants'] = 'polyester'
        self.assertEqual('polyester', self.pa['pants'])


class MappingPathAccessorTests (MPABaseMixin, PathAccessorBaseTests):
    TargetClass = MappingPathAccessor

    def test_keys(self):
        self.assertEqual({'weapon', 'armor', 'get'}, set(self.pa.keys()))

    def test_get(self):
        self.assertEqual('sword', self.pa.get('weapon'))
        self.assertEqual(None, self.pa.get('hat'))
        self.assertEqual('gru', self.pa.get('sidekick', 'gru'))

    def test_update(self):
        self.pa.update({'hat': 'wizard', 'belt': 'cowboy'})
        expectedkeys = {'weapon', 'armor', 'get', 'hat', 'belt'}
        self.assertEqual(expectedkeys, self.pa.keys())


class MappedAttrsPathAccessorTests (MPABaseMixin, PathAccessorBaseTests):
    TargetClass = MappedAttrsPathAccessor

    def test_attribute_access_versus_getitem(self):
        self.assertEqual('leather', self.pa.armor)
        self.assertEqual('leather', self.pa['armor'])

    def test_tricky_attribute_access(self):
        thing1 = self.pa.get
        thing2 = self.pa['get']
        self.assertEqual('got', thing1)
        self.assertEqual(thing1, thing2)

    def test_setattr_versus_setitem(self):
        self.pa.hat = 'wizard'
        self.assertEqual('wizard', self.pa.hat)
        self.assertEqual('wizard', self.pa['hat'])

        self.pa['hat'] = 'tophat'
        self.assertEqual('tophat', self.pa.hat)
        self.assertEqual('tophat', self.pa['hat'])

    def test_mapa_to_mapping_interface(self):
        # If you need a Mapping interface use this API:
        mpa = MappingPathAccessor.fromMappedAttrs(self.pa)
        self.assertEqual('leather', mpa.get('armor'))
        self.assertEqual('got', mpa.get('get'))
        self.assertEqual('banana', mpa.get('fruit', 'banana'))


class SequencePathAccessorTests (PathAccessorBaseTests):
    TargetClass = SequencePathAccessor
    TargetValue = ['a', 'b', 'c']

    def test_getitem(self):
        self.assertEqual('b', self.pa[1])

    def test_getitem_keyerror(self):
        self.assertRaisesRegexp(
            KeyError,
            r"^<[A-Za-z]+PathAccessor ROOT {.*}> has no member 42$",
            self.pa.__getitem__,
            42,
        )

    def test_setitem(self):
        self.pa['pants'] = 'polyester'
        self.assertEqual('polyester', self.pa['pants'])


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

    def test_compound_write_mappedattrs(self):
        mapa = MappedAttrsPathAccessor(self.structure, 'ROOT')
        mapa.a[0].bar = 'banana'

        self.assertEqual(
            {
                'a': [{
                    "foo": [None, [], 1337],
                    "bar": 'banana',
                }],
            },
            self.structure,
        )

    def test_compound_write_sequence(self):
        mapa = MappedAttrsPathAccessor(self.structure, 'ROOT')
        mapa.a[0].foo[0] = 'banana'

        self.assertEqual(
            {
                'a': [{
                    "foo": ['banana', [], 1337],
                }],
            },
            self.structure,
        )
