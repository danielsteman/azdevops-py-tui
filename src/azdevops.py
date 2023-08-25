import os
from typing import List

from azure.devops.connection import Connection
from azure.devops.v7_0.git.git_client import GitClient
from azure.devops.v7_0.git.models import GitRepository
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication

load_dotenv()


class AzDevopsManager:
    """
    Example usage:
    man = AzDevopsManager("analyticslab-p", "asrnl")
    print(man.get_repositories())
    >>>
    [...]
    """

    def __init__(self, project: str, organization: str) -> None:
        self.project = project
        self.pat = os.environ["PERSONAL_ACCESS_TOKEN"]
        self.git_client = self.get_git_client(self.pat, organization)

    @classmethod
    def get_git_client(self, pat: str, organization: str) -> GitClient:
        organization_url = f"https://dev.azure.com/{organization}"
        credentials = BasicAuthentication("", pat)
        connection = Connection(base_url=organization_url, creds=credentials)
        git_client = connection.clients.get_git_client()
        return git_client

    def get_repositories(self, sort_on_name: bool = True) -> List[GitRepository]:
        repositories = self.git_client.get_repositories(project=self.project)
        if sort_on_name:
            return sorted(repositories, key=lambda repo: repo.name)
        return repositories

    def get_remote_url_with_pat(self, repository) -> str:
        prefix, suffix = repository.remote_url.split("@", 1)
        return f"{prefix}:{self.pat}@{suffix}"
