import sys
import argparse


def main(args=sys.argv[1:]):
    """
    Track the attribute/index/key path into a dicts-and-lists data structure.
    """
    opts = parse_args(args)
    raise NotImplementedError(main)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)
    return p.parse_args(args)
