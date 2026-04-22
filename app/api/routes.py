import time
from fastapi import APIRouter
from app.models.schemas import SolveRequest, SolveResponse
from app.core.classifier import TaskClassifier
from app.core.registry import registry
from app.core.verifier import OutputVerifier
from app.core.logger import logger
# Import solvers to register them
from app.models.enums import TaskType
from app.solvers.math_solver import MathSolver
from app.solvers.extraction_solver import ExtractionSolver
from app.solvers.classification_solver import ClassificationSolver
from app.solvers.list_ops_solver import ListOpsSolver
from app.solvers.comparison_solver import ComparisonSolver
from app.solvers.rule_engine_solver import RuleEngineSolver
from app.solvers.poly_gcd_solver import PolyGCDSolver
from app.solvers.definite_integral_solver import DefiniteIntegralSolver
from app.solvers.llm_fallback import LLMFallbackSolver

router = APIRouter()

# 1. Register our Solvers into the central registry
registry.register(TaskType.ARITHMETIC, MathSolver())
registry.register(TaskType.EXTRACTION, ExtractionSolver())
registry.register(TaskType.CLASSIFICATION, ClassificationSolver())
registry.register(TaskType.LIST_OPS, ListOpsSolver())
registry.register(TaskType.COMPARISON, ComparisonSolver())
registry.register(TaskType.RULE_ENGINE, RuleEngineSolver())
registry.register(TaskType.DEFINITE_INTEGRAL, DefiniteIntegralSolver())
registry.register(TaskType.POLY_GCD, PolyGCDSolver())
registry.set_fallback(LLMFallbackSolver())

@router.post("/v1/answer", response_model=SolveResponse)
async def solve_endpoint(request: SolveRequest):
    start_time = time.time()
    error_msg = None
    final_output = None
    solver_name = "None"
    task_type = TaskType.UNKNOWN
    
    try:
        # 2. Classification
        task_type = TaskClassifier.classify(request.query, request.assets)
        
        # 3. Routing (Get Solver)
        solver = registry.get_solver(task_type)
        solver_name = solver.name
        
        # 4. Execution
        raw_output = await solver.solve(request.query, request.assets)
        
        # If the mapped solver failed, run the fallback explicitly (hybrid strategy)
        if raw_output is None and solver != registry._fallback_solver:
            logger.info(f"Solver {solver_name} yielded None. Triggering fallback.")
            solver = registry._fallback_solver
            solver_name = solver.name
            raw_output = await solver.solve(request.query, request.assets)
        
        # 5. Verification & Formatting
        final_output = OutputVerifier.verify_and_format(raw_output)
        
    except Exception as e:
        error_msg = str(e)
        final_output = "An internal error occurred."
    
    # 6. Observability Logging
    latency = time.time() - start_time
    logger.log_request(
        query=request.query,
        asset_count=len(request.assets),
        task_type=task_type.name,
        solver=solver_name,
        latency=latency,
        output_len=len(final_output) if final_output else 0,
        error=error_msg
    )
    
    return SolveResponse(output=final_output)
