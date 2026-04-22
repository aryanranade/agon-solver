import re
from typing import List, Optional, Dict
from app.solvers.base import BaseSolver
from app.core.logger import logger

class ComparisonSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level5_ComparisonSolver"

    @staticmethod
    def _extract_name_value_pairs(query: str) -> Dict[str, float]:
        """
        Extracts name→value pairs from phrases like:
        "Alice scored 80, Bob scored 90."
        "Alice is 170cm tall, Bob is 165cm."
        "Alice has 5 apples, Bob has 12."
        "Alice got a score of 95, Bob got 88."
        """
        pairs = {}
        
        # Strategy 1: Direct — "[Name] [verb] [optional filler] [number]"
        # Allows up to 4 optional words between verb and number (handles "a score of")
        matches = re.findall(
            r'\b([A-Z][a-z]+)\b(?:\s+\w+){1,5}?\s+(\d+(?:\.\d+)?)\b',
            query
        )
        for name, value in matches:
            if name.lower() in {'who', 'what', 'which', 'where', 'when', 'how'}:
                continue
            # Don't overwrite an earlier pair for the same name
            if name not in pairs:
                pairs[name] = float(value)

        return pairs

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q = query.lower()
        pairs = self._extract_name_value_pairs(query)

        if len(pairs) < 2:
            return None

        # Determine comparison direction
        # "highest, most, tallest, oldest, fastest, largest, greatest, more, best, first, longest, heaviest, richest, max"
        want_max = re.search(
            r'\b(highest|most|tallest|oldest|fastest|largest|greatest|more|best|first|longest|heaviest|richest|maximum|max|bigger|bigger|stronger|better)\b',
            q
        )
        # "lowest, least, shortest, youngest, slowest, smallest, fewer, worst, last, lightest, minimum, min"
        want_min = re.search(
            r'\b(lowest|least|shortest|youngest|slowest|smallest|fewer|fewest|worst|last|lightest|minimum|min|smaller|weaker|worse)\b',
            q
        )

        if want_max:
            winner = max(pairs, key=pairs.__getitem__)
            return winner
        elif want_min:
            winner = min(pairs, key=pairs.__getitem__)
            return winner

        # Fallback: if "who scored" or "who has" detected, default to max
        if re.search(r'\bwho\b', q):
            winner = max(pairs, key=pairs.__getitem__)
            return winner

        return None
