from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Tree, Static, Checkbox
from textual.containers import Container, VerticalScroll, HorizontalScroll
from textual import work
from services import github_api as gha


class GitOnlyThis(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 30%;
        border-right: solid $primary;
        background: $surface;
    }

    #main-area {
        width: 70%;
    }

    #repo-input {
        width: 100%;
        margin-bottom: 1;
    }

    #open-btn {
        width: 100%;
        margin-bottom: 1;
    }

    #file-tree {
        height: 100%;
    }

    #action-bar {
        height: auto;
        dock: bottom;
        border-top: solid $primary;
        padding: 1;
    }
    """

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

            self._load_filepaths(url)
            self.notify(message=f"loading: {url}")
    
    @work(thread=True)
    def _load_filepaths(self, repo_url: str):
        filepaths = gha.get_repo_filepaths(repo_url)
        self.call_from_thread(self._populate_file_tree, filepaths)


    def _populate_file_tree(self, filepaths: list[str]):
        file_tree = self.query_one("#file-tree")
        file_tree.remove_children()
        for path in filepaths:
            file_tree.mount(Checkbox(path))
        
        self.notify("loaded!")


if __name__ == "__main__":
    app = GitOnlyThis()
    app.run()