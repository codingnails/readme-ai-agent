from langchain_core.tools import tool
from app.chains.overview_chain import overview_readme
from app.chains.refine_chain import refine_readme
from app.chains.review_chain import review_readme

@tool
def overview_tool(repo_summary: dict) -> str:
    """Generate draft README overview based on repo summary."""
    print("Overview tool called")
    return overview_readme(repo_summary["repo_name"], repo_summary["code_entities"])

@tool
def refine_tool(draft_text: str, previous_readme: str, review_report: str) -> str:
    """Refine the draft README text to improve formatting and remove duplicates."""
    print("Refine tool called")
    return refine_readme(draft_text, previous_readme, review_report)

@tool
def review_tool(draft_text: str, refined_text: str) -> str:
    """Generate review report comparing draft and refined README."""
    print("Review tool called")
    return review_readme(draft_text, refined_text)
