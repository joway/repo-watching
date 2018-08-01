# Repo Watching

Github repos watching framework

## Install

```shell
pip install watching
```

## Simple Usage

function `ctx.upsert_file_and_pr` is a helper to update or create file and create pull request .

```python
watcher = Watcher({
    'github_access_token': ACCESS_TOKEN,
})


def license_middleware(ctx: Context):
    branch = 'watcher_license_create'
    path = '/LICENSE'
    commits = ctx.repo.commit_list()
    newest_commit = commits[0]
    new_content = 'MIT\n\ncreated by joway'
    message = 'add MIT license'
    pr_title = 'Init: MIT License'
    pr_body = '- create MIT License'

    file_branch = 'master'

    ctx.upsert_file_and_pr(
        path=path, content=new_content, branch=branch,
        should_upsert=lambda new, old: new != old, message=message,
        pr_title=pr_title, pr_body=pr_body,
    )


def other_middleware(ctx: Context):
    pass


def filter_func(repo: Repo):
    if repo.name == 'repo-watching-demo':
        return True


# task chain , it will be executed by every repo
watcher.use(license_middleware, other_middleware)

# filter the repos you need
repos = watcher.get_all_repos(filter_func=filter_func)

# listen repos
watcher.listen(repos)

# traverse all repos you listened
watcher.run()

```

## Advanced Usage

```python
# get commit list
ctx.repo.commit_list()

# access your github username | org name
ctx.repo.login
ctx.repo.name

# create file
ctx.repo.file_create()
# update file
ctx.repo.file_update()
# get file
ctx.repo.file_get()
# create branch
ctx.repo.branch_create()
# create pr
ctx.repo.pr_create()
```