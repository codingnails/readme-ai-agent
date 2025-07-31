from app.chains.overview_chain import overview_readme
from app.chains.refine_chain import refine_readme
from app.chains.review_chain import review_readme
from app.utils.folder_structure import generate_folder_structure
from app.utils.static_sections import generate_installation_section, generate_usage_section, generate_additional_info_section


class ReadmeGenerator:
    """
    Combines AI (LangChain) and static sections to create a complete README.
    """
    def generate_overview(self, repo_summary):
        """
        Calls LangChain chain to generate an overview from repo_summary.
        """
        code_entities = self._list_code_entities(repo_summary)
        draft_text = overview_readme(repo_summary.repo_name, code_entities)
        return draft_text

    def _list_code_entities(self, repo_summary):
        lines = []
        if repo_summary.classes:
            lines.append("Classes:")
            for cls in repo_summary.classes:
                lines.append(f"- {cls.name}: {cls.summary or 'No summary'}")
        if repo_summary.functions:
            lines.append("Functions:")
            for fn in repo_summary.functions:
                lines.append(f"- {fn.name}: {fn.summary or 'No summary'}")
        return "\n".join(lines)

    def generate_refine(self, draft_text, previous_readme=None, review_report=None):
        refined_text = refine_readme(draft_text, previous_readme=previous_readme, review_report=review_report)
        return refined_text

    def generate_review(self, draft_text, refined_text):
        review_content, quality_score = review_readme(draft_text, refined_text)
        return review_content, quality_score

    def generate_readme_markdown(self, repo_summary, repo_path, previous_readme=None, review_report=None):
        draft_text = self.generate_overview(repo_summary)
        refined_text = self.generate_refine(draft_text, previous_readme=previous_readme, review_report=review_report)
        review_content, quality_score = self.generate_review(draft_text, refined_text)

        sections = [
            f"# {repo_summary.repo_name}\n",
            "## Overview\n\n" + refined_text + "\n",
            "## Folder Structure\n\n```\n" + generate_folder_structure(repo_path) + "\n```\n",
            generate_installation_section(),
            generate_usage_section(),
            generate_additional_info_section(),
        ]

        readme_markdown = "\n".join(sections)
        return readme_markdown, review_content, quality_score
