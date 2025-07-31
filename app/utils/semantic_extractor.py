from typing import Optional
from openai import OpenAI
from app.models.repo_summary import RepoSummary

class SemanticExtractor:
    """
    Uses LLM (OpenAI GPT) to generate human-readable summaries
    for functions and classes in the RepoSummary.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def summarize(self, repo_summary: RepoSummary) -> RepoSummary:
        """
        Loops through functions/classes in RepoSummary and generates summaries.
        Returns enriched RepoSummary.
        """
        
        for func in repo_summary.functions:
            func.summary = self._summarize_function(func.name, func.args, func.docstring)

        for cls in repo_summary.classes:
            cls.summary = self._summarize_class(cls.name, cls.docstring, cls.methods)
            
            for method in cls.methods:
                method.summary = self._summarize_function(method.name, method.args, method.docstring)

        return repo_summary

    def _summarize_function(self, name: str, args: list, docstring: Optional[str]) -> str:
        """
        Call GPT to summarize a function.
        """
        prompt = (
            f"Summarize this Python function:\n"
            f"Name: {name}\n"
            f"Arguments: {args}\n"
            f"Docstring: {docstring or 'No docstring provided'}\n"
            f"Provide a short, clear description in one sentence."
        )

        response = self.client.responses.create(
            model=self.model_name,
            input=prompt
        )

        return response.output_text.strip()

    def _summarize_class(self, name: str, docstring: Optional[str], methods: list) -> str:
        """
        Call GPT to summarize a class.
        """
        method_names = [m.name for m in methods]
        prompt = (
            f"Summarize this Python class:\n"
            f"Name: {name}\n"
            f"Docstring: {docstring or 'No docstring provided'}\n"
            f"Methods: {method_names}\n"
            f"Provide a short, clear description in one sentence."
        )

        response = self.client.responses.create(
            model=self.model_name,
            input=prompt
        )

        return response.output_text.strip()
