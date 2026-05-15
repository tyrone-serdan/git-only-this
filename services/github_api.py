from github import Github

gh = Github()

class RepoFetcher:
    def __init__(self, repo_url: str):
        self.repo = gh.get_repo(parse_url(repo_url))

    def get_file_content(self, filepath: str) -> str:
        try:
            contents = self.repo.get_contents(filepath)
            return contents.decoded_content.decode() # type: ignore
        except:
            return "Cannot display file :("

    def get_repo_filepaths(self) -> list[str]:
        files: list[str] = []

        branch = self.repo.get_branch(self.repo.default_branch)

        # TODO: make user select which commit/branch to download from (?)
        tree = self.repo.get_git_tree(
            branch.commit.sha,
            recursive=True
        )

        for item in tree.tree:
            if item.type == "blob":
                files.append(item.path)

        return files

    def download_file(self, filepath: str):
        file = self.repo.get_contents(filepath)

        return file

def parse_url(url: str) -> str:
    # TODO: actually make the implementation
    # ______________________________________
    # Possible inputs by a user:
    #     https://github.com/user/repository
    #     https://github.com/tyrone-serdan/minimal-blog-astro/
    #     https://github.com/tyrone-serdan/minimal-blog-astro.git
    #     git@github.com:tyrone-serdan/minimal-blog-astro.git
    # _________________________________________________________
    #    the package im using will only accept:
    #        tyrone-serdan/minimal-blog-astro
    parsed: str = url

    return parsed

