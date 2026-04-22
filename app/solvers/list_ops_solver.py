import re
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

class ListOpsSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level4_ListOpsSolver"

    @staticmethod
    def _extract_numbers(query: str) -> List[int]:
        """Extract the list of numbers from 'Numbers: 2,5,8,11.' style prefix."""
        match = re.search(r'numbers?:?\s*([\d,\s]+)', query, re.IGNORECASE)
        if match:
            raw = match.group(1)
            return [int(n.strip()) for n in re.findall(r'\d+', raw)]
        # Fallback: grab all numbers from entire string
        return [int(n) for n in re.findall(r'\b\d+\b', query)]

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q = query.lower()
        nums = self._extract_numbers(query)
        if not nums:
            return None

        evens = [n for n in nums if n % 2 == 0]
        odds  = [n for n in nums if n % 2 != 0]

        # --- Sum operations ---
        if re.search(r'sum even', q):
            return str(sum(evens))

        if re.search(r'sum odd', q):
            return str(sum(odds))

        if re.search(r'sum (?:all|the)?\s*(?:numbers?|them)?\.?$', q) or re.search(r'sum of all', q):
            return str(sum(nums))

        if re.search(r'sum', q):   # generic sum fallback
            return str(sum(nums))

        # --- Count operations ---
        if re.search(r'count even', q):
            return str(len(evens))

        if re.search(r'count odd', q):
            return str(len(odds))

        if re.search(r'count', q):
            return str(len(nums))

        # --- Max / min ---
        if re.search(r'(?:find |get )?max(?:imum)?', q):
            return str(max(nums))

        if re.search(r'(?:find |get )?min(?:imum)?', q):
            return str(min(nums))

        # --- Average / mean ---
        if re.search(r'average|mean', q):
            avg = sum(nums) / len(nums)
            return str(int(avg)) if avg == int(avg) else str(round(avg, 2))

        # --- Sort ---
        if re.search(r'sort.*desc', q):
            return ', '.join(str(n) for n in sorted(nums, reverse=True))

        if re.search(r'sort', q):
            return ', '.join(str(n) for n in sorted(nums))

        # --- Product ---
        if re.search(r'product|multiply', q):
            result = 1
            for n in nums: result *= n
            return str(result)

        # --- Largest / smallest (synonyms for max/min) ---
        if re.search(r'largest|greatest|biggest|highest', q):
            return str(max(nums))

        if re.search(r'smallest|lowest|least', q):
            return str(min(nums))

        # --- Range ---
        if re.search(r'range', q):
            return str(max(nums) - min(nums))

        return None
