import os

def generate_folder_structure(repo_path: str, max_depth: int = 1) -> str:
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