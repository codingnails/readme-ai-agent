# app/agents/code_extractor.py
import ast
import os
from typing import List

from app.models.function_info import FunctionInfo
from app.models.class_info import ClassInfo
from app.models.repo_summary import RepoSummary

class CodeExtractor:
    """
    Parses Python files in a repo directory and extracts structured info about classes and functions.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []

    def extract(self) -> RepoSummary:
        """
        Main entry point: walk repo and extract info.
        """
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    self._parse_file(filepath)

        # Repo name from path basename (can improve later)
        repo_name = os.path.basename(os.path.normpath(self.repo_path))

        return RepoSummary(
            repo_name=repo_name,
            functions=self.functions,
            classes=self.classes
        )

    def _parse_file(self, filepath: str) -> None:
        """
        Parse a single Python file with ast and extract functions/classes.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:
            # Skip files with syntax errors for now
            return

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._extract_function(node)
                self.functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._extract_class(node)
                self.classes.append(class_info)

    def _extract_function(self, node: ast.FunctionDef) -> FunctionInfo:
        """
        Extract info from a function node.
        """
        name = node.name
        args = [arg.arg for arg in node.args.args]
        docstring = ast.get_docstring(node)
        start_line = node.lineno
        end_line = getattr(node, 'end_lineno', start_line)  # Python 3.8+

        return FunctionInfo(
            name=name,
            args=args,
            docstring=docstring,
            start_line=start_line,
            end_line=end_line
        )

    def _extract_class(self, node: ast.ClassDef) -> ClassInfo:
        """
        Extract info from a class node, including methods.
        """
        name = node.name
        docstring = ast.get_docstring(node)
        start_line = node.lineno
        end_line = getattr(node, 'end_lineno', start_line)

        methods = []
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                method_info = self._extract_function(child)
                methods.append(method_info)

        return ClassInfo(
            name=name,
            methods=methods,
            docstring=docstring,
            start_line=start_line,
            end_line=end_line
        )
