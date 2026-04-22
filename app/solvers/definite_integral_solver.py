import re
from typing import List, Optional, Tuple
from app.solvers.base import BaseSolver
from app.core.logger import logger

# Unicode subscript/superscript digit maps
_SUB = '₀₁₂₃₄₅₆₇₈₉'
_SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹'
_SUB_MAP = {c: str(i) for i, c in enumerate(_SUB)}
_SUP_MAP = {c: str(i) for i, c in enumerate(_SUP)}


def _normalize_expr(text: str) -> str:
    """Normalize unicode math to ASCII for the integrand."""
    text = text.replace('−', '-').replace('–', '-').replace('—', '-')
    for sup, digit in _SUP_MAP.items():
        text = text.replace(sup, '^' + digit)
    return text


class DefiniteIntegralSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "DefiniteIntegralSolver"

    @staticmethod
    def _extract(query: str) -> Optional[Tuple[float, float, str]]:
        """Return (lower, upper, normalized_integrand) or None."""
        integral_pos = query.find('∫')

        if integral_pos != -1:
            pos = integral_pos + 1
            while pos < len(query) and query[pos] == ' ':
                pos += 1
            if pos < len(query) and query[pos] == '_':
                pos += 1

            # Read lower limit
            lower_str = ''
            if pos < len(query) and query[pos] in _SUB:
                while pos < len(query) and query[pos] in _SUB:
                    lower_str += _SUB_MAP[query[pos]]
                    pos += 1
            else:
                m = re.match(r'-?\d+(?:\.\d+)?', query[pos:])
                if m:
                    lower_str = m.group()
                    pos += len(lower_str)

            if pos < len(query) and query[pos] == '^':
                pos += 1

            # Read upper limit
            upper_str = ''
            if pos < len(query) and query[pos] in _SUP:
                while pos < len(query) and query[pos] in _SUP:
                    upper_str += _SUP_MAP[query[pos]]
                    pos += 1
            else:
                m = re.match(r'-?\d+(?:\.\d+)?', query[pos:])
                if m:
                    upper_str = m.group()
                    pos += len(upper_str)

            if not lower_str or not upper_str:
                return None

            rest = query[pos:]
            dx_m = re.search(r'\s*dx\b', rest, re.IGNORECASE) or re.search(r'dx', rest, re.IGNORECASE)
            if not dx_m:
                return None

            integrand = _normalize_expr(rest[:dx_m.start()].strip())
            return float(lower_str), float(upper_str), integrand

        # Fallback: "from X to Y" text form
        m = re.search(
            r'integral\s+(?:of\s+)?(.+?)\s+from\s+(-?\d+(?:\.\d+)?)\s+to\s+(-?\d+(?:\.\d+)?)',
            query, re.IGNORECASE
        )
        if m:
            return float(m.group(2)), float(m.group(3)), _normalize_expr(m.group(1).strip())

        return None

    @staticmethod
    def _parse_poly(expr: str) -> List[Tuple[float, float]]:
        """Parse polynomial string into list of (coefficient, exponent) pairs."""
        e = expr.strip()
        # Remove outer parens
        while True:
            inner = re.match(r'^\s*\((.+)\)\s*$', e)
            if inner:
                e = inner.group(1).strip()
            else:
                break

        # Implicit multiplication: "2x" → "2*x"
        e = re.sub(r'(\d)(x)', r'\1*\2', e, flags=re.IGNORECASE)

        if not e.startswith('-'):
            e = '+' + e

        parts = re.findall(r'[+\-][^+\-]+', e)
        terms = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            sign = -1.0 if part[0] == '-' else 1.0
            body = part[1:].strip()

            if 'x' in body.lower():
                xi = body.lower().find('x')
                coeff_str = body[:xi].strip().rstrip('* ').strip()
                rest = body[xi + 1:].strip()
                coeff = 1.0 if coeff_str in ('', '+') else float(coeff_str)
                coeff *= sign
                exp = 1.0
                if rest.startswith('^'):
                    try:
                        exp = float(rest[1:].strip().split()[0])
                    except (ValueError, IndexError):
                        exp = 1.0
                terms.append((coeff, exp))
            else:
                try:
                    terms.append((float(body.strip()) * sign, 0.0))
                except ValueError:
                    pass
        return terms

    @staticmethod
    def _antiderivative(terms: List[Tuple[float, float]], x: float) -> float:
        return sum((c / (n + 1)) * (x ** (n + 1)) for c, n in terms)

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q_lower = query.lower()
        if 'integral' not in q_lower and '∫' not in query:
            return None

        extracted = self._extract(query)
        if extracted is None:
            return None
        lower, upper, integrand = extracted

        terms = self._parse_poly(integrand)
        if not terms:
            return None

        result = self._antiderivative(terms, upper) - self._antiderivative(terms, lower)
        logger.info(f"Integral: [{lower},{upper}] '{integrand}' terms={terms} result={result}")

        if abs(result - round(result)) < 1e-9:
            return str(int(round(result)))
        return str(round(result, 6)).rstrip('0').rstrip('.')
