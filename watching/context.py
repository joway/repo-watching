import logging.config
import typing

from github import Repository

from watching.exceptions import BranchExistError, FileNotExistError, PRExistError

logger = logging.getLogger(__name__)


class Context:
    def __init__(self, repo: Repository):
        self.repo = repo

    def upsert_file_and_pr(
            self, path, content, branch,
            should_upsert: typing.Callable, message, pr_title,
            pr_body, base_branch='master',
    ):
        file_branch = 'master'
        commits = self.repo.commit_list()
        newest_commit = commits[0]

        # create branch
        try:
            self.repo.branch_create(branch=branch, sha=newest_commit.sha)
        except BranchExistError:
            file_branch = branch
            logger.error(f'branch {branch} existed')

        # upsert file
        try:
            file = self.repo.file_get(path, branch=file_branch)
            # modify file content
            old_content = file.content
            if should_upsert(content, old_content):
                self.repo.file_update(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch,
                    sha=file.sha,
                )
        except FileNotExistError:
            self.repo.file_create(
                path=path,
                message=message,
                content=content,
                branch=branch,
            )

        # create pull request
        try:
            return self.repo.pr_create(
                title=pr_title,
                body=pr_body,
                branch=branch,
                base=base_branch,
            )
        except PRExistError:
            logger.error('pr existed')
