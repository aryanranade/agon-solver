from abc import ABC, abstractmethod
from typing import List, Optional

class BaseSolver(ABC):
    """
    The interface contract for all solvers.
    Any new strategy added must implement the solve() method.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the solver plugin for logging purposes."""
        pass
        
    @abstractmethod
    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        """
        Executes the solver logic.
        Should return a clean string if successful, or None if the solver cannot handle the query.
        """
        pass
