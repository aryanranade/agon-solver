from pydantic import BaseModel, Field
from typing import List, Optional

class SolveRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = Field(default_factory=list)

class SolveResponse(BaseModel):
    output: str
