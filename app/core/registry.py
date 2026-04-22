from typing import Type, Dict
from app.models.enums import TaskType
from app.solvers.base import BaseSolver
from app.core.logger import logger

class SolverRegistry:
    """Central registry to map TaskType to specific Solver implementations."""
    
    _registry: Dict[TaskType, BaseSolver] = {}
    _fallback_solver: BaseSolver = None
    
    @classmethod
    def register(cls, task_type: TaskType, solver: BaseSolver):
        cls._registry[task_type] = solver
        logger.info(f"Registry: Mapped {task_type.name} to {solver.name}")
        
    @classmethod
    def set_fallback(cls, solver: BaseSolver):
        cls._fallback_solver = solver
        logger.info(f"Registry: Set fallback to {solver.name}")
        
    @classmethod
    def get_solver(cls, task_type: TaskType) -> BaseSolver:
        """Returns the mapped solver, or the fallback if not explicitly mapped/unknown."""
        solver = cls._registry.get(task_type)
        if solver:
            return solver
        return cls._fallback_solver

registry = SolverRegistry()
