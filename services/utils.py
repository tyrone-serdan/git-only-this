def language_from_path(path: str) -> str | None:
    ext = path.rsplit(".", 1)[-1] if "." in path else ""
    mapping = {
        "py": "python",
        "js": "javascript",
        "html": "html",
        "css": "css",
        "json": "json",
        "md": "markdown",
        "rs": "rust",
        "go": "go",
        "java": "java",
        "xml": "xml",
        "yaml": "yaml",
        "yml": "yaml",
        "sql": "sql",
        "sh": "bash",
        "bash": "bash",
        "toml": "toml",
    }
    return mapping.get(ext)