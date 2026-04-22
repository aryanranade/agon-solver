import re
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

class PolyGCDSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level11_PolyGCDSolver"

    @staticmethod
    def _extract_roots(poly_text: str) -> set:
        """
        Extracts roots from a polynomial expressed as a product of linear factors.
        Handles:
          (x-3)(x-4)(x+5)(x-6)    → {3, 4, -5, 6}
          (x - 3)(x - 4)           → {3, 4}
          (x+2)(x-7)               → {-2, 7}
        """
        # Match (x - N) or (x + N) or (x-N) or (x+N)
        matches = re.findall(r'\(\s*x\s*([+-])\s*(\d+)\s*\)', poly_text)
        roots = set()
        for sign, val in matches:
            # (x - 3) has root x = +3; (x + 3) has root x = -3
            root = int(val) if sign == '-' else -int(val)
            roots.add(root)
        return roots

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q_lower = query.lower()

        # Only handle polynomial GCD degree queries
        if not ('gcd' in q_lower and 'degree' in q_lower):
            return None

        # Normalize unicode minus/dash variants to regular ASCII minus
        query = query.replace('−', '-').replace('–', '-').replace('—', '-')

        # Split on q(x) = to separate the two polynomials
        # Pattern: "p(x) = <poly1> q(x) = <poly2>"
        split = re.split(r'q\s*\(x\)\s*=', query, flags=re.IGNORECASE)
        if len(split) < 2:
            return None

        left_part  = split[0]  # contains p(x) = ...
        right_part = split[1]  # contains q(x) factors

        # Extract p(x) part: everything after "p(x) ="
        p_split = re.split(r'p\s*\(x\)\s*=', left_part, flags=re.IGNORECASE)
        if len(p_split) < 2:
            return None

        p_factors = p_split[1].strip()
        q_factors = right_part.strip()

        # Extract roots from each polynomial
        p_roots = self._extract_roots(p_factors)
        q_roots = self._extract_roots(q_factors)

        logger.info(f"PolyGCD: p_roots={sorted(p_roots)}, q_roots={sorted(q_roots)}")

        # GCD degree = number of common roots (each with min multiplicity)
        common = p_roots & q_roots
        degree = len(common)

        logger.info(f"PolyGCD: common_roots={sorted(common)}, degree={degree}")
        return str(degree)
