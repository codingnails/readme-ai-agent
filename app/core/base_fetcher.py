from abc import ABC, abstractmethod

class BaseRepoFetcher(ABC):
    """Abstract base class for all repo fetching strategies (git, API, etc.)."""

    @abstractmethod
    def fetch_repo(self, repo_url: str) -> str:
        """
        Fetch the repository and return the local path where it is stored.
        """
        pass

    @abstractmethod
    def cleanup_repo(self) -> None:
        """
        Clean up any temporary files or directories used during fetching.
        """
        pass
