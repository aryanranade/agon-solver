import re
from typing import List, Optional, Dict
from app.solvers.base import BaseSolver
from app.core.logger import logger


class PolyGCDSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level11_PolyGCDSolver"

    @staticmethod
    def _parse_factors(text: str) -> Dict[str, int]:
        """
        Extract {root_str: multiplicity} from a factored polynomial expression.
        Handles: (x-3), (x+5), (2x-6), (-x+3), (x-3)^2, (x-3)^{2}
        """
        factors: Dict[str, int] = {}
        pattern = re.compile(
            r'\(\s*(-?\d*)\s*[a-zA-Z]\s*([+\-])\s*(\d+)\s*\)'   # (ax ± b)
            r'(?:\s*\^?\s*\{?\s*(\d+)\s*\}?)?',                   # optional ^N or ^{N}
        )
        for m in pattern.finditer(text):
            a_raw, sign, b_str, pow_str = m.group(1), m.group(2), m.group(3), m.group(4)
            a = 1 if a_raw in ('', '+') else (-1 if a_raw == '-' else int(a_raw))
            if a == 0:
                continue
            b = int(b_str) * (1 if sign == '+' else -1)
            root = -b / a  # ax + b = 0 → x = -b/a
            key = str(round(root * 1_000_000) / 1_000_000)
            factors[key] = factors.get(key, 0) + (int(pow_str) if pow_str else 1)
        return factors

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q_lower = query.lower()
        if 'gcd' not in q_lower or 'degree' not in q_lower:
            return None

        # Normalize unicode minus/dash to ASCII
        q = query.replace('−', '-').replace('–', '-').replace('—', '-')

        # Extract polynomial definitions: any letter(x) = <expr>
        defs = []
        def_re = re.compile(
            r'(?:^|[\s,])\s*[a-zA-Z]\s*\(\s*[a-zA-Z]\s*\)\s*=\s*(.+?)'
            r'(?=\s+[a-zA-Z]\s*\(\s*[a-zA-Z]\s*\)\s*=|\bcompute\b|\bfind\b'
            r'|\bwhat\b|\bgcd\b|\bdegree\b|\.\s|$)',
            re.IGNORECASE | re.DOTALL
        )
        for m in def_re.finditer(q):
            expr = m.group(1).strip()
            if '(' in expr:  # only accept factored forms
                defs.append(expr)

        if len(defs) >= 2:
            fa = self._parse_factors(defs[0])
            fb = self._parse_factors(defs[1])
        else:
            # Try inline: gcd((x-1)(x-2), (x-2)(x-3))
            inline = re.search(
                r'gcd\s*\(\s*([^,)].+?)\s*,\s*([^)].+?)\s*\)',
                q, re.IGNORECASE
            )
            if not inline:
                return None
            fa = self._parse_factors(inline.group(1))
            fb = self._parse_factors(inline.group(2))

        if not fa or not fb:
            return None

        # Degree of GCD = sum of min(multiplicity_p, multiplicity_q) per shared root
        degree = sum(min(fa[r], fb.get(r, 0)) for r in fa)

        logger.info(f"PolyGCD: fa_roots={sorted(fa)}, fb_roots={sorted(fb)}, degree={degree}")
        return str(degree)
