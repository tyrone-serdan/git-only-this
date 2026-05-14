from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, Checkbox
from textual.containers import Container, VerticalScroll
from textual import work, on
from services import github_api as gha
from services import downloader as d


class GitOnlyThis(App):
    CSS_PATH = "app.tcss"
    filepaths: list[str] = []
    current_repo: str = ''

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="sidebar"):
            yield Input(placeholder="Repository URL or path", id="repo-input")
            yield Button("Open Repository", id="open-btn")
            yield Static("\nFiles", id="files-header")
            with VerticalScroll(id="file-tree"):
                yield Static("Enter a repository URL to browse", id="placeholder")
        with Container(id="main-area"):
            with VerticalScroll():
                yield Static("Select files from the sidebar to see details", id="details")
        with Container(id="action-bar"):
            yield Button("Download Selected", id="download-btn", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open-btn":
            repo_input = self.query_one("#repo-input", Input)
            url = repo_input.value

            self.current_repo = url
            self._load_filepaths(url)
            self.notify(message=f"loading: {url}")
        
        if event.button.id == "download-btn":
            self._download_files(self.current_repo, self.filepaths)

    
    @work(thread=True)
    def _load_filepaths(self, repo_url: str):
        filepaths = gha.get_repo_filepaths(repo_url)
        self.call_from_thread(self._populate_file_tree, filepaths)


    @work(thread=True)
    def _download_files(self, repo_url: str, filepaths: list[str]) -> None:
        d.download_files(repo_url, filepaths)
        self.call_from_thread(self.notify, "Download complete!")

    def _populate_file_tree(self, filepaths: list[str]):
        file_tree = self.query_one("#file-tree")
        file_tree.remove_children()
        for path in filepaths:
            file_tree.mount(Checkbox(path))
        
        self.notify("loaded!")

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        checkbox = event.checkbox
        
        is_checked = checkbox.value

        if is_checked:
            self.filepaths.append(checkbox.label._text)
        else:
            self.filepaths.remove(checkbox.label._text)

        self.notify(str(self.filepaths))

if __name__ == "__main__":
    app = GitOnlyThis()
    app.run()