from app.agents.repo_fetcher import RepoFetcher
from app.agents.code_extractor import CodeExtractor
from app.agents.semantic_extractor import SemanticExtractor
from app.agents.readme_generator import ReadmeGenerator
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Main entry point for the project.

    Clones the specified repository, extracts code information, generates semantic
    summaries, and generates a README.md file. Finally, it cleans up the cloned
    repository.

    """
    repo_url = "https://github.com/codingnails/pdf-assistant-rag-weaviate"

    # Step 1: Clone the repo
    fetcher = RepoFetcher()
    local_path = fetcher.fetch_repo(repo_url)
    print(f"Repo cloned to: {local_path}")

    # Step 2: Extract code info
    extractor = CodeExtractor(local_path,repo_url)
    repo_summary = extractor.extract()

    # Phase 2: Semantic Summaries
    api_key = os.getenv("OPENAI_API_KEY")
    semantic_extractor = SemanticExtractor(api_key)
    enriched_summary = semantic_extractor.summarize(repo_summary)

    # Step 4: Save README.md
    readme_gen = ReadmeGenerator()
    readme_md, review_report = readme_gen.generate_readme_markdown(enriched_summary, local_path)

    with open(os.path.join(local_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_md)

    print("README.md generated successfully at: " , local_path)

    # Step 5: Cleanup
    fetcher.cleanup_repo()
    print("Repo cleaned up successfully")

if __name__ == "__main__":
    main()
