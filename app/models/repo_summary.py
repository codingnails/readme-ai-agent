from pydantic import BaseModel
from typing import List
from .class_info import ClassInfo
from .function_info import FunctionInfo

class RepoSummary(BaseModel):
    repo_name: str
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
