import sys
from typing import Tuple

__all__ = ["errorln"]


def errorln(loc: Tuple[str, int, int], *msg):
    """General error with newline"""
    f, ln, col = loc
    print(f"{f}:{ln}:{col}:", *msg, file=sys.stderr)
    sys.exit(1)
