from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, Checkbox, TextArea, Collapsible
from textual.containers import Container, VerticalScroll
from textual import work, on
from services.github_api import RepoFetcher
from services import downloader as d
from services import utils


class GitOnlyThis(App):
    CSS_PATH = "app.tcss"
    filepaths: list[str] = []
    repo_fetcher: RepoFetcher | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="sidebar"):
            yield Input(placeholder="Repository URL or path", id="repo-input")
            yield Button("Open Repository", id="open-btn")
            yield Static("\nFiles", id="files-header")
            with VerticalScroll(id="file-tree"):
                yield Static("Enter a repository URL to browse", id="placeholder")

        with Container(id="main-area"):
            yield TextArea(id="details", read_only=True)

        with Container(id="action-bar"):
            yield Button("Download Selected", id="download-btn", variant="primary")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open-btn":
            repo_input = self.query_one("#repo-input", Input)
            url = repo_input.value

            self.repo_fetcher = RepoFetcher(url)
            self._load_filepaths()
            self.notify(message=f"loading: {url}")
        
        if event.button.id == "download-btn" and self.repo_fetcher:
            self._download_files(self.repo_fetcher, self.filepaths)

    
    @work(thread=True)
    def _load_filepaths(self):
        if not self.repo_fetcher:
            return
        filepaths = self.repo_fetcher.get_repo_filepaths()
        self.call_from_thread(self._populate_file_tree, filepaths)


    @work(thread=True)
    def _download_files(self, fetcher, filepaths: list[str]) -> None:
        d.download_files(fetcher, filepaths)
        self.call_from_thread(self.notify, "Download complete!")

    def _populate_file_tree(self, filepaths: list[str]):
        file_tree = self.query_one("#file-tree")
        file_tree.remove_children()

        tree = self._build_tree(filepaths)
        widgets = self._build_collapsible_widgets(tree)

        for widget in widgets:
            file_tree.mount(widget)

        self.notify("loaded!")

    def _build_tree(self, paths: list[str]) -> dict:
        tree = {}
        for path in sorted(paths):
            parts = path.split("/")
            current = tree

            for i, part in enumerate(parts):
                if part not in current:
                    if i == len(parts) - 1:
                        current[part] = None
                    else:
                        current[part] = {}
                    
                current = current[part]
            
        return tree

    def _build_collapsible_widgets(self, tree: dict, prefix: str = "") -> list:
        widgets = []
        for key in sorted(tree, key=lambda k: (not isinstance(tree[k], dict), k)):
            value = tree[key]
            path = f"{prefix}{key}" if prefix else key

            if value is None:
                widgets.append(Checkbox(path))
            else:
                children = self._build_collapsible_widgets(value, f"{path}/")
                widgets.append(Collapsible(*children, title=f"📁 {key}/"))
        
        return widgets

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        checkbox = event.checkbox
        is_checked = checkbox.value

        filepath = checkbox.label._text

        if is_checked:
            self.filepaths.append(filepath)
        else:
            self.filepaths.remove(filepath)
        
        self._load_file_content(filepath)

    @work(thread=True)
    def _load_file_content(self, filepath: str) -> None:
        if not self.repo_fetcher:
            return
        content = self.repo_fetcher.get_file_content(filepath)
        self.call_from_thread(self._display_content, content, filepath)

    def _display_content(self, content: str, filepath: str) -> None:
        textarea = self.query_one("#details", TextArea)
        language = utils.language_from_path(filepath)

        if language and language in textarea.available_languages:
            textarea.language = language
        else:
            textarea.language = None
        
        textarea.text = content

if __name__ == "__main__":
    app = GitOnlyThis()
    app.run()