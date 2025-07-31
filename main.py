from app.core.repo_fetcher import RepoFetcher
from app.core.code_extractor import CodeExtractor
from app.utils.semantic_extractor import SemanticExtractor
from app.agents.readme_agent import ReadmeGenerator
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Main entry point for the project.

    Clones the specified repository, extracts code information, generates semantic
    summaries, and generates a README.md file. Uses a refine and review loop to
    improve the README quality. Finally, it cleans up the cloned repository.

    """
    repo_url = "https://github.com/codingnails/pdf-assistant-rag-weaviate"

    # Step 1: Clone the repo
    fetcher = RepoFetcher()
    local_path = fetcher.fetch_repo(repo_url)
    print(f"Repo cloned to: {local_path}")

    # Step 2: Extract code info (one-time process)
    extractor = CodeExtractor(local_path,repo_url)
    repo_summary = extractor.extract()

    # Phase 2: Semantic Summaries (one-time process)
    api_key = os.getenv("OPENAI_API_KEY")
    semantic_extractor = SemanticExtractor(api_key)
    enriched_summary = semantic_extractor.summarize(repo_summary)

    # Initialize README generator and start refine-review loop
    readme_gen = ReadmeGenerator()
    readme_md = None
    review_report = None
    max_iterations = 3  # Maximum number of refine-review cycles
    current_iteration = 0

    while current_iteration < max_iterations:
        print(f"\nStarting refine-review iteration {current_iteration + 1}/{max_iterations}")
        
        # Generate or refine README
        readme_md, review_report, quality_score = readme_gen.generate_readme_markdown(
            enriched_summary,
            local_path,
            previous_readme=readme_md,
            review_report=review_report
        )
        
        # Save the current version
        readme_path = os.path.join(local_path, f"README_v{current_iteration + 1}.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_md)
        
        print(f"README version {current_iteration + 1} generated at: {readme_path}")
        
        # Check if review report indicates sufficient quality
        if quality_score >= 0.9:
            print("README quality is sufficient. Ending refine-review loop.")
            break
            
        current_iteration += 1

    # Save final README as README.md
    final_readme_path = os.path.join(local_path, "README.md")
    with open(final_readme_path, "w", encoding="utf-8") as f:
        f.write(readme_md)
    print(f"Final README.md generated at: {final_readme_path}")

    # Step 5: Cleanup
    fetcher.cleanup_repo()
    print("Repo cleaned up successfully")

if __name__ == "__main__":
    main()
