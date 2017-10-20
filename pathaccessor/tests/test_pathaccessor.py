import unittest
import re
from pathaccessor import MappingPathAccessor


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


class CompoundStructureTests (PathAccessorBaseTests):
    def test_member_error(self):
        mpa = MappingPathAccessor({'a': [{"foo": [None, []]}]}, 'ROOT')
        child = mpa['a'][0]['foo'][1]
        self.assertRaisesLiteral(
            TypeError,
            ("Index 'bananas' of "
             + "<SequencePathAccessor ROOT['a'][0]['foo'][1] []>"
             + " not an integer"),
            child.__getitem__,
            'bananas',
        )
