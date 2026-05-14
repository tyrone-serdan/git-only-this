from pathlib import Path
from services import github_api as gha


def download_files(repo_url: str, filepaths: list[str]) -> None:
    repo_name = repo_url.strip("/").split("/")[-1]
    default_path = Path.home() / "Downloads" / repo_name

    for filepath in filepaths:
        file = gha.download_file(repo_url, filepath)
        content = file.decoded_content # type: ignore

        output_path = default_path / filepath
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(content)
        

