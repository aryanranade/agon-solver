import re
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

class ClassificationSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level3_ClassificationSolver"
    
    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2: return False
        if n == 2: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0: return False
        return True

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q = query.lower().strip()
        
        # Pattern 1: Is X odd/even?
        odd_match = re.search(r'is (\d+) an? odd', q)
        if odd_match:
            n = int(odd_match.group(1))
            return "YES" if n % 2 != 0 else "NO"
        
        even_match = re.search(r'is (\d+) an? even', q)
        if even_match:
            n = int(even_match.group(1))
            return "YES" if n % 2 == 0 else "NO"

        # Pattern 2: Is X prime?
        prime_match = re.search(r'is (\d+) (?:a )?prime', q)
        if prime_match:
            n = int(prime_match.group(1))
            return "YES" if self._is_prime(n) else "NO"

        # Pattern 3: Is X divisible by Y?
        div_match = re.search(r'is (\d+) divisible by (\d+)', q)
        if div_match:
            n, d = int(div_match.group(1)), int(div_match.group(2))
            return "YES" if (d != 0 and n % d == 0) else "NO"

        # Pattern 4: Is X greater than Y? / Is X less than Y?
        gt_match = re.search(r'is (\d+) (?:greater|more|larger|bigger) than (\d+)', q)
        if gt_match:
            return "YES" if int(gt_match.group(1)) > int(gt_match.group(2)) else "NO"

        lt_match = re.search(r'is (\d+) (?:less|smaller|fewer) than (\d+)', q)
        if lt_match:
            return "YES" if int(lt_match.group(1)) < int(lt_match.group(2)) else "NO"

        # Pattern 5: Is X a perfect square?
        sq_match = re.search(r'is (\d+) a perfect square', q)
        if sq_match:
            n = int(sq_match.group(1))
            return "YES" if int(n**0.5) ** 2 == n else "NO"

        # Pattern 6: Is X a factor of Y? / Is X a multiple of Y?
        factor_match = re.search(r'is (\d+) a factor of (\d+)', q)
        if factor_match:
            a, b = int(factor_match.group(1)), int(factor_match.group(2))
            return "YES" if (a != 0 and b % a == 0) else "NO"

        multiple_match = re.search(r'is (\d+) a multiple of (\d+)', q)
        if multiple_match:
            n, m = int(multiple_match.group(1)), int(multiple_match.group(2))
            return "YES" if (m != 0 and n % m == 0) else "NO"

        # Pattern 7: Is X positive/negative?
        pos_match = re.search(r'is (-?\d+) (?:a )?positive', q)
        if pos_match:
            return "YES" if int(pos_match.group(1)) > 0 else "NO"

        neg_match = re.search(r'is (-?\d+) (?:a )?negative', q)
        if neg_match:
            return "YES" if int(neg_match.group(1)) < 0 else "NO"

        # Pattern 8: Is X equal to Y?
        eq_match = re.search(r'is (\d+) equal to (\d+)', q)
        if eq_match:
            return "YES" if int(eq_match.group(1)) == int(eq_match.group(2)) else "NO"

        return None
