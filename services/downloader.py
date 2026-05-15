from pathlib import Path
from services.github_api import RepoFetcher


def download_files(fetcher: RepoFetcher, filepaths: list[str]) -> None:
    repo_name = fetcher.repo.full_name.split("/")[-1]
    default_path = Path.home() / "Downloads" / repo_name

    for filepath in filepaths:
        file = fetcher.download_file(filepath)
        content = file.decoded_content # type: ignore

        output_path = default_path / filepath
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(content)
