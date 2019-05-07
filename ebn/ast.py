from enum import Enum, auto
from typing import Tuple, Any, TypeVar, Generic

__all__ = ("TypeEnum", "Type", "TermEnum", "Term", "SemEnum", "Sem")

EnumT = TypeVar("EnumT")


class AstNode(Generic[EnumT]):
    info: Tuple[str, int, int]
    e: EnumT
    v: Any

    def __init__(self, e: EnumT, v: Any):
        self.info = ("<stdin>", 0, 0)
        self.e = e
        self.v = v

    def __repr__(self):
        return f"AstNode(Type={self.e}, Value={self.v})"


class TypeEnum(Enum):
    Unit = auto()
    Arrow = auto()
    Prod = auto()


class Type(AstNode[TypeEnum]):
    """Basic type"""


class TermEnum(Enum):
    Var = auto()
    Lam = auto()
    App = auto()
    Pair = auto()
    Fst = auto()
    Snd = auto()


class Term(AstNode[TermEnum]):
    """Syntactic term"""


class SemEnum(Enum):
    Lam = auto()
    Pair = auto()
    Syn = auto()


class Sem(AstNode[SemEnum]):
    """Semantic term"""
