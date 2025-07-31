from git import Repo
import tempfile
import shutil
import os
from app.core.base_fetcher import BaseRepoFetcher

class RepoFetcher(BaseRepoFetcher):
    """
    Git-based repository fetcher.
    Performs shallow clone (depth=1) for performance and cleanup handling.
    """

    def __init__(self, cleanup: bool = True):
        self.cleanup = cleanup
        self._cloned_path = None

    def fetch_repo(self, repo_url: str) -> str:
        """
        Clone the repository (shallow) and return local path.
        """
        
        temp_dir = tempfile.mkdtemp(prefix="repo_")
        self._cloned_path = temp_dir

        Repo.clone_from(repo_url, temp_dir, depth=1)
        return temp_dir

    def cleanup_repo(self) -> None:
        """
        Delete the cloned repository directory if cleanup enabled.
        """
        if self.cleanup and self._cloned_path and os.path.exists(self._cloned_path):
            shutil.rmtree(self._cloned_path)
            self._cloned_path = None
