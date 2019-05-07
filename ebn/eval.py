from __future__ import annotations

from typing import Any, Dict, Optional
from .ast import TypeEnum, Type, TermEnum, Term, SemEnum, Sem
from .util import errorln

__all__ = ("reflect", "reify", "meaning", "nbe")


class Ctx:
    """Typing context"""

    def __init__(self):
        self._d: Dict[str, Any] = {}

    def lookup(self, tm: Term) -> Any:
        k = tm.v
        try:
            return self._d[k]
        except KeyError:
            errorln(tm.info, f"no such variable '{k}'")

    def add(self, k: str, v: Any) -> Ctx:
        if k in self._d:
            errorln(v.info, f"variable '{k}' already defined")
        self._d[k] = v
        return self


_VAR = 0


def _fresh_var() -> str:
    """Retrieve a fresh variable"""
    global _VAR
    var = str(_VAR)
    _VAR += 1
    return var


def reflect(ty: Type, tm: Term) -> Sem:
    """Reflects the term syntax to the semantics"""
    if ty.e == TypeEnum.Arrow:
        arg_t, ret_t = ty.v
        return Sem(
            SemEnum.Lam,
            lambda s: reflect(
                ret_t, Term(TermEnum.App, (tm, reify(arg_t, s)))
            ),
        )
    elif ty.e == TypeEnum.Prod:
        a, b = ty.v
        return Sem(
            SemEnum.Pair,
            (
                reflect(a, Term(TermEnum.Fst, tm)),
                reflect(b, Term(TermEnum.Snd, tm)),
            ),
        )
    elif ty.e == TypeEnum.Unit:
        return Sem(SemEnum.Syn, tm)

    return errorln(tm.info, "IMPOSSIBLE")


def reify(ty: Type, sem: Sem) -> Term:
    """Reifies the semantics as a syntactic term"""
    if ty.e == TypeEnum.Arrow and sem.e == SemEnum.Lam:
        arg_t, ret_t = ty.v
        fn = sem.v
        x = _fresh_var()
        return Term(
            TermEnum.Lam,
            (x, reify(ret_t, fn(reflect(arg_t, Term(TermEnum.Var, x))))),
        )
    elif ty.e == TypeEnum.Prod and sem.e == SemEnum.Pair:
        a_t, b_t = ty.v
        a, b = sem.v
        return Term(TermEnum.Pair, (reify(a_t, a), reify(b_t, b)))
    elif ty.e == TypeEnum.Unit and sem.e == SemEnum.Syn:
        return sem.v

    return errorln(ty.info, f"reify error: type '{ty}', semantic '{sem}')")


def meaning(ctx: Ctx, tm: Term) -> Sem:
    """Evaluation"""
    if tm.e == TermEnum.Var:
        return ctx.lookup(tm)
    elif tm.e == TermEnum.Lam:
        arg, body = tm.v
        return Sem(SemEnum.Lam, lambda s: meaning(ctx.add(arg, s), body))
    elif tm.e == TermEnum.App:
        s, t = tm.v
        fn = meaning(ctx, s)
        if fn.e != SemEnum.Lam:
            errorln(fn.info, f"eval error: {fn} is not a lambda function")
        return fn.v(meaning(ctx, t))
    elif tm.e == TermEnum.Pair:
        a, b = tm.v
        return Sem(SemEnum.Pair, (meaning(ctx, a), meaning(ctx, b)))
    elif tm.e == TermEnum.Fst:
        pair = meaning(ctx, tm.v)
        if pair.e != SemEnum.Pair:
            errorln(pair.info, f"eval error: {pair} is not a pair")
        a, _ = pair.v
        return Sem(SemEnum.Pair, a)
    elif tm.e == TermEnum.Snd:
        pair = meaning(ctx, tm.v)
        if pair.e != SemEnum.Pair:
            errorln(pair.info, f"eval errorln: {pair} is not a pair")
        _, b = pair.v
        return Sem(SemEnum.Pair, b)

    return errorln(tm.info, f"eval errorln: ctx '{ctx}', term '{tm}'")


def nbe(ty: Type, tm: Term) -> Term:
    """Normalization"""
    return reify(ty, meaning(Ctx(), tm))
