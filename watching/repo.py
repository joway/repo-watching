import logging.config

from github import Repository, GithubException, UnknownObjectException

from watching.exceptions import FileNotExistError, FileExistError, BranchExistError, PRExistError
from watching.file import File

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class Repo:
    def __init__(self, repo: Repository):
        self._repo: Repository = repo

    @property
    def login(self):
        return self._repo.owner.login

    @property
    def name(self):
        return self._repo.name

    def file_create(self, path, message, content, branch):
        logger.info(f'file create : path "{path}", message "{message}", content "{content}", branch "{branch}"')
        try:
            return self._repo.create_file(
                path=path,
                message=message,
                content=content,
                branch=branch,
            )
        except GithubException as e:
            logger.error(e)
            raise FileExistError

    def file_get(self, path, branch='master'):
        logger.info(f'file get : path "{path}", branch "{branch}"')
        try:
            return File(self._repo.get_file_contents(path, ref=f'refs/heads/{branch}'))
        except UnknownObjectException as e:
            logger.error(e)
            raise FileNotExistError

    def file_update(self, path, message, content, branch, sha):
        logger.info(
            f'file update : path "{path}", message "{message}", content "{content}", branch "{branch}", sha "{sha}"'
        )
        return self._repo.update_file(
            path=path,
            message=message,
            content=content,
            sha=sha,
            branch=branch,
        )

    def commit_list(self):
        return self._repo.get_commits()

    def branch_create(self, branch, sha):
        logger.info(f'branch create : branch "{branch}", sha "{sha}"')
        try:
            return self._repo.create_git_ref(ref=f'refs/heads/{branch}', sha=sha)
        except GithubException as e:
            logger.error(e)
            raise BranchExistError

    def pr_create(self, title, body, branch, base):
        logger.info(f'pr create : title "{title}", body "{body}", branch "{branch}", base "{base}"')
        try:
            return self._repo.create_pull(
                title=title,
                body=body,
                head=branch,
                base=base,
            )
        except GithubException as e:
            logger.error(e)
            raise PRExistError
