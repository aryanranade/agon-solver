import logging
import json
from datetime import datetime

# Setup basic logging to stdout
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
_base_logger = logging.getLogger("agon_solver")

class StructuredLogger:
    @staticmethod
    def log_request(query: str, asset_count: int, task_type: str, solver: str, latency: float, output_len: int, error: str = None):
        """Emits a structured JSON log for easy extraction/monitoring during iteratons."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "asset_count": asset_count,
            "task_type": task_type,
            "solver": solver,
            "latency_ms": round(latency * 1000, 2),
            "output_length": output_len,
        }
        if error:
            log_data["error"] = error
            _base_logger.error(json.dumps(log_data))
        else:
            _base_logger.info(json.dumps(log_data))
            
    @staticmethod
    def info(msg: str):
        _base_logger.info(msg)
        
    @staticmethod
    def error(msg: str):
        _base_logger.error(msg)

logger = StructuredLogger()
