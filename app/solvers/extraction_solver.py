import re
from typing import List, Optional
from app.solvers.base import BaseSolver
from app.core.logger import logger

class ExtractionSolver(BaseSolver):
    @property
    def name(self) -> str:
        return "Deterministic_Level2_ExtractionSolver"
        
    async def solve(self, query: str, assets: List[str]) -> Optional[str]:
        q_lower = query.lower()
        
        # 1. Date Extraction: "Meeting on 12 March 2024" -> "12 March 2024"
        if 'date' in q_lower:
            # Matches DD Month YYYY, e.g., "12 March 2024"
            date_match = re.search(r'(\d{1,2}\s+[a-zA-Z]+\s+\d{4})', query)
            if date_match:
                return date_match.group(1).strip()
                
            # Matches YYYY-MM-DD
            iso_match = re.search(r'(\d{4}-\d{2}-\d{2})', query)
            if iso_match:
                return iso_match.group(1).strip()
                
            # Matches MM/DD/YYYY or DD/MM/YYYY
            slash_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', query)
            if slash_match:
                return slash_match.group(1).strip()
                
        # 2. Email Extraction
        if 'email' in q_lower:
            email_match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', query)
            if email_match:
                return email_match.group(1).strip()
                
        # 3. Phone Number Extraction
        if 'phone' in q_lower or 'number' in q_lower:
            # Matches common formats like +1-555-123-4567 or (555) 123-4567
            phone_match = re.search(r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})', query)
            if phone_match:
                return phone_match.group(1).strip()
                
        # 4. Amount / Currency Extraction
        if 'amount' in q_lower or 'price' in q_lower or 'cost' in q_lower:
            cost_match = re.search(r'(\$?\d+(?:,\d{3})*(?:\.\d{2})?)', query)
            if cost_match:
                return cost_match.group(1).strip()

        # Let the Groq fallback handle unstructured extraction
        return None
