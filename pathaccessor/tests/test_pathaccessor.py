import unittest
import re
from pathaccessor import MappingPathAccessor, MappedAttrsPathAccessor


class PathAccessorBaseTests (unittest.TestCase):
    def assertRaisesLiteral(self, exc, msg, f, *args, **kw):
        self.assertRaisesRegexp(
            exc,
            '^{}$'.format(re.escape(msg)),
            f,
            *args,
            **kw
        )


class MappingPathAccessorTests (PathAccessorBaseTests):
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


class CompoundStructureTests (PathAccessorBaseTests):
    def setUp(self):
        self.structure = {'a': [{"foo": [None, []]}]}

    def test_mapping(self):
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

    def test_mappedattrs(self):
        mpa = MappedAttrsPathAccessor(self.structure, 'ROOT')
        child = mpa['a'][0].foo[1]
        self.assertRaisesLiteral(
            TypeError,
            ("Index 'bananas' of "
             + "<SequencePathAccessor ROOT['a'][0].foo[1] []>"
             + " not an integer"),
            child.__getitem__,
            'bananas',
        )
