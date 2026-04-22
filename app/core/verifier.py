from app.config import settings
from app.core.logger import logger

from typing import Optional

class OutputVerifier:
    @staticmethod
    def verify_and_format(raw_output: Optional[str]) -> str:
        """
        Validates the output string.
        - Ensures it is not None/empty
        - Strips whitespace
        - Truncates if it exceeds the maximum safe limit for the evaluator.
        """
        if not raw_output:
            logger.error("Verification failed: Output is empty.")
            return "No answer found."
            
        cleaned = str(raw_output).strip()
        
        # Failsafe limit to avoid massive context dumps ruining evaluations
        if len(cleaned) > settings.MAX_OUTPUT_LENGTH:
            logger.error(f"Verification warning: Output truncated from {len(cleaned)} to {settings.MAX_OUTPUT_LENGTH} chars.")
            # We don't just abruptly cut off mid-word, but for a hackathon, hard truncate is usually fine.
            cleaned = cleaned[:settings.MAX_OUTPUT_LENGTH]
            
        return cleaned
