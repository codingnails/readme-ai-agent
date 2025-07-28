# app/models/function_info.py
from pydantic import BaseModel
from typing import List, Optional

class FunctionInfo(BaseModel):
    name: str
    args: List[str]
    docstring: Optional[str]
    start_line: int
    end_line: int
    summary: Optional[str] = None
