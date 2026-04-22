import re
import ast
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

_SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹'
_SUP_MAP = {c: str(i) for i, c in enumerate(_SUP)}


def _sup_to_digits(s: str) -> str:
    return ''.join(_SUP_MAP.get(c, c) for c in s)


def _mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def _mat_pow(M, p):
    size = len(M)
    result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    base = [row[:] for row in M]
    while p > 0:
        if p & 1:
            result = _mat_mul(result, base)
        base = _mat_mul(base, base)
        p >>= 1
    return result


class MatrixTraceSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "MatrixTraceSolver"

    @staticmethod
    def _parse_matrix(query: str):
        m = re.search(r'(\[\s*\[[\d\s,\-]+\](?:\s*,\s*\[[\d\s,\-]+\])*\s*\])', query)
        if not m:
            return None
        try:
            return ast.literal_eval(m.group(1))
        except Exception:
            return None

    @staticmethod
    def _parse_exponent(query: str) -> Optional[int]:
        # trace(M⁸) — superscript digits
        m = re.search(r'trace\s*\(\s*\w+([⁰¹²³⁴⁵⁶⁷⁸⁹]+)\s*\)', query)
        if m:
            return int(_sup_to_digits(m.group(1)))
        # trace(M^8) or trace(M^{8})
        m = re.search(r'trace\s*\(\s*\w+\s*\^\s*\{?(\d+)\}?\s*\)', query)
        if m:
            return int(m.group(1))
        return None

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        if 'trace' not in query.lower():
            return None

        matrix = self._parse_matrix(query)
        if matrix is None:
            return None

        n = self._parse_exponent(query)
        if n is None:
            return None

        powered = _mat_pow(matrix, n)
        trace_val = sum(powered[i][i] for i in range(len(powered)))

        logger.info(f"MatrixTrace: size={len(matrix)} exp={n} trace={trace_val}")
        return str(trace_val)
