def generate_installation_section() -> str:
        return (
            "## Installation\n\n"
            "```bash\n"
            "python3 -m venv venv\n"
            "source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`\n"
            "pip install -r requirements.txt\n"
            "```\n"
        )

def generate_usage_section() -> str:
        return (
            "## Usage\n\n"
            "Run the main script after cloning the repo:\n\n"
            "```bash\n"
            "python main.py\n"
            "```\n"
        )

def generate_additional_info_section() -> str:
    return (
        "## Additional Information\n\n"
        "For more details, please refer to the documentation or contact the maintainers through the issue tracker.\n"
    )