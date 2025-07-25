from app.agents.repo_fetcher import RepoFetcher
from app.agents.code_extractor import CodeExtractor

def main():
    repo_url = "https://github.com/codingnails/cpt-ai-code-assistant.git"

    # Step 1: Clone the repo
    fetcher = RepoFetcher()
    local_path = fetcher.fetch_repo(repo_url)
    print(f"Repo cloned to: {local_path}")

    # Step 2: Extract code info
    extractor = CodeExtractor(local_path)
    repo_summary = extractor.extract()

    # Step 3: Print summary as JSON
    print(repo_summary.model_dump_json(indent=2))

    # Step 4: Cleanup
    fetcher.cleanup_repo()

if __name__ == "__main__":
    main()
