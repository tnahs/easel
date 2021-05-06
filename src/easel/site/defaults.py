class Extensions:
    YAML: tuple[str, ...] = (
        ".yaml",
        ".yml",
    )
    IMAGE: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    )
    VIDEO: tuple[str, ...] = (
        ".mp4",
        ".webm",
        ".mov",
    )
    AUDIO: tuple[str, ...] = (
        ".mp3",
        ".wav",
    )
    MARKDOWN: tuple[str, ...] = (
        ".md",
        ".markdown",
        ".txt",
    )
    CONTENT: tuple[str, ...] = (
        *IMAGE,
        *VIDEO,
        *AUDIO,
        *MARKDOWN,
    )
