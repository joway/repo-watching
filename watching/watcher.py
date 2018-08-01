import logging
import typing

from github import Github

from watching.context import Context
from watching.exceptions import AccessTokenError
from watching.repo import Repo

logger = logging.getLogger(__name__)


def _get_or_default(d: dict, k, default):
    if k in d:
        return d[k]
    return default


class Watcher:
    def __init__(self, config: dict):
        github_access_token = _get_or_default(config, 'github_access_token', None)
        if github_access_token is None:
            raise AccessTokenError

        self.client = Github(github_access_token)
        self.tasks = []
        self.listening_repos = []

    def listen(self, *args):
        self.listening_repos.extend(*args)

    def use(self, *args):
        self.tasks.extend(args)

    def run(self):
        for repo in self.listening_repos:
            for func in self.tasks:
                ctx = Context(repo=repo)
                func(ctx)

    def get_all_repos(self, filter_func: typing.Callable = None):
        results = self.client.get_user().get_repos()
        repos = []
        for repo in results:
            _repo = Repo(repo)
            if filter_func and not filter_func(_repo):
                continue
            repos.append(_repo)
        logger.info(f'get all repos : found {len(repos)} repos')
        return repos
