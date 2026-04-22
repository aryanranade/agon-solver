import re
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

class KnowledgeListSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level9_KnowledgeListSolver"

    # ── Static knowledge bases ──────────────────────────────────────────────
    DAYS_ALL     = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
    DAYS_WEEK    = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
    DAYS_WEEKEND = ["SATURDAY","SUNDAY"]

    MONTHS_ALL   = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
                    "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
    MONTHS_31    = ["JANUARY","MARCH","MAY","JULY","AUGUST","OCTOBER","DECEMBER"]
    MONTHS_30    = ["APRIL","JUNE","SEPTEMBER","NOVEMBER"]
    MONTHS_28_29 = ["FEBRUARY"]

    SEASONS      = ["SPRING","SUMMER","AUTUMN","WINTER"]
    PLANETS      = ["MERCURY","VENUS","EARTH","MARS","JUPITER","SATURN","URANUS","NEPTUNE"]
    CONTINENTS   = ["AFRICA","ANTARCTICA","ASIA","AUSTRALIA","EUROPE","NORTH AMERICA","SOUTH AMERICA"]
    VOWELS       = ["A","E","I","O","U"]
    PRIMARY_COL  = ["RED","BLUE","YELLOW"]
    SECONDARY_COL= ["GREEN","ORANGE","PURPLE"]
    RAINBOW      = ["RED","ORANGE","YELLOW","GREEN","BLUE","INDIGO","VIOLET"]

    @staticmethod
    def _fmt(items: List[str]) -> str:
        return "|".join(items)

    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q = query.lower()

        # Must contain "list" or "output" to be this type
        if not re.search(r'\blist\b|\boutput\b|\bname\b', q):
            return None
        # Must specify pipe-separated or uppercase style
        if not re.search(r'pipe|uppercase|uppercas|\bupper\b', q):
            return None

        # ── Days ──────────────────────────────────────────────────────────
        if 'weekend' in q:
            return self._fmt(self.DAYS_WEEKEND)

        if re.search(r'weekday|working day|work day', q):
            return self._fmt(self.DAYS_WEEK)

        if re.search(r'all days|days of the week', q):
            return self._fmt(self.DAYS_ALL)

        # ── Months ────────────────────────────────────────────────────────
        if re.search(r'31 days|thirty.one days', q):
            return self._fmt(self.MONTHS_31)

        if re.search(r'30 days|thirty days', q):
            return self._fmt(self.MONTHS_30)

        if re.search(r'28|29|february|leap', q) and 'month' in q:
            return self._fmt(self.MONTHS_28_29)

        if re.search(r'months? of the year|all months?|twelve months?', q):
            return self._fmt(self.MONTHS_ALL)

        # ── Other knowledge lists ──────────────────────────────────────────
        if 'season' in q:
            return self._fmt(self.SEASONS)

        if 'planet' in q:
            return self._fmt(self.PLANETS)

        if 'continent' in q:
            return self._fmt(self.CONTINENTS)

        if 'vowel' in q:
            return self._fmt(self.VOWELS)

        if re.search(r'primary colo', q):
            return self._fmt(self.PRIMARY_COL)

        if re.search(r'secondary colo', q):
            return self._fmt(self.SECONDARY_COL)

        if re.search(r'rainbow|colors? of the rainbow', q):
            return self._fmt(self.RAINBOW)

        # Fallback to Groq for unlisted knowledge queries
        return None
