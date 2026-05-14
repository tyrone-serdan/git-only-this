from github import Github

gh = Github()

def parse_url(url: str) -> str:
	# TODO: actually make the implementation
	# ______________________________________
	# Possible inputs by a user:
	# 	https://github.com/user/repository
	#		https://github.com/tyrone-serdan/minimal-blog-astro/
	# 	https://github.com/tyrone-serdan/minimal-blog-astro.git
	#		git@github.com:tyrone-serdan/minimal-blog-astro.git
	# _________________________________________________________
	#	the package im using will only accept:
	#		tyrone-serdan/minimal-blog-astro
	parsed: str = url

	return parsed



def get_repo_filepaths(repo_link: str) -> list[str]:
	files: list[str] = []
	repo = gh.get_repo(parse_url(repo_link))

	branch = repo.get_branch(repo.default_branch)

	# TODO: make user select which commit/branch to download from (?)
	tree = repo.get_git_tree(
		branch.commit.sha,
		recursive=True
	)

	for item in tree.tree:
		if item.type == "blob":
			files.append(item.path)

	return files