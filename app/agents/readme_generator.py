import os
from app.chains.overview_chain import overview_readme
from app.chains.refine_chain import refine_readme
from app.chains.review_chain import review_readme

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

    def generate_refine(self, draft_text):
        refined_text = refine_readme(draft_text)
        return refined_text

    def generate_review(self, draft_text, refined_text):
        review = review_readme(draft_text, refined_text)
        return review

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

    def generate_folder_structure(self, repo_path: str, max_depth: int = 1) -> str:
        """
        Generate folder tree up to max_depth (ignores virtualenv/cache dirs).
        """
        ignore_dirs = {".git", "__pycache__", "venv", ".venv", ".env", ".idea"}

        def walk(dir_path, prefix="", depth=0):
            if depth > max_depth:
                return ""
            entries = sorted(
                e for e in os.listdir(dir_path)
                if e not in ignore_dirs and not e.startswith(".")
            )
            lines = []
            for i, entry in enumerate(entries):
                path = os.path.join(dir_path, entry)
                connector = "├── " if i < len(entries) - 1 else "└── "
                lines.append(f"{prefix}{connector}{entry}")
                if os.path.isdir(path):
                    extension = "│   " if i < len(entries) - 1 else "    "
                    lines.append(walk(path, prefix + extension, depth + 1))
            return "\n".join(lines)

        tree_str = f"{os.path.basename(os.path.normpath(repo_path))}/\n"
        tree_str += walk(repo_path)
        return tree_str

    def generate_installation_section(self) -> str:
        return (
            "## Installation\n\n"
            "```bash\n"
            "python3 -m venv venv\n"
            "source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`\n"
            "pip install -r requirements.txt\n"
            "```\n"
        )

    def generate_usage_section(self) -> str:
        return (
            "## Usage\n\n"
            "Run the main script after cloning the repo:\n\n"
            "```bash\n"
            "python main.py\n"
            "```\n"
        )

    def generate_additional_info_section(self) -> str:
        return (
            "## Additional Information\n\n"
            "For more details, please refer to the documentation or contact the maintainers through the issue tracker.\n"
        )

    def generate_readme_markdown(self, repo_summary, repo_path):
        draft_text = self.generate_overview(repo_summary)
        refined_text = self.generate_refine(draft_text)
        review_report = self.generate_review(draft_text, refined_text)

        sections = [
            f"# {repo_summary.repo_name}\n",
            "## Overview\n\n" + refined_text + "\n",
            "## Folder Structure\n\n```\n" + self.generate_folder_structure(repo_path) + "\n```\n",
            self.generate_installation_section(),
            self.generate_usage_section(),
            self.generate_additional_info_section(),
        ]

        readme_markdown = "\n".join(sections)
        return readme_markdown, review_report
