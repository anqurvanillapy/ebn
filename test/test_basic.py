import unittest
from ebn.ast import TypeEnum, Type, TermEnum, Term, SemEnum, Sem
from ebn.eval import reflect, reify, meaning, nbe


class TestBasic(unittest.TestCase):
    def test_id(self):
        x = Term(TermEnum.Lam, ("x", Term(TermEnum.Var, "x")))
        result = nbe(
            Type(
                TypeEnum.Arrow,
                (Type(TypeEnum.Unit, None), Type(TypeEnum.Unit, None)),
            ),
            x,
        )
        expected = Term(TermEnum.Lam, ("0", Term(TermEnum.Var, "0")))
        self.assertEqual(result, expected)

    def test_k(self):
        k = Term(
            TermEnum.Lam,
            ("x", Term(TermEnum.Lam, ("y", Term(TermEnum.Var, "x")))),
        )
        x = Term(TermEnum.Lam, ("x", Term(TermEnum.Var, "x")))
        _ = nbe(
            Type(
                TypeEnum.Arrow,
                (Type(TypeEnum.Unit, None), Type(TypeEnum.Unit, None)),
            ),
            Term(TermEnum.App, (k, x)),
        )
