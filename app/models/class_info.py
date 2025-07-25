from pydantic import BaseModel
from typing import List, Optional
from .function_info import FunctionInfo

class ClassInfo(BaseModel):
    name: str
    methods: List[FunctionInfo]
    docstring: Optional[str]
    start_line: int
    end_line: int
