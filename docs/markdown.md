# Markdown

<!--

## Inserting Images

When inserting images into a Markdown page or a Markdown content type item all paths must be relative to the parent page folder. With a structure like this:

``` plaintext
[site]
└── pages
    ├── ...
    └── [markdown-page]
        ├── page.yaml
        ├── page-description.md
        ├── 000-note.md
        ├── 001-entry
        │   ├── body.md
        │   └── images
        │       └── 800x400.png
        └── 002-entry
            ├── body.md
            └── 1920x1080.png
```

The image `800x400.png` in `001-entry/images` would require the path `001-entry/images/800x400.png` to render correctly while `1920x1080.png` in `002-entry` would only require the path `002-entry/1920x1080.png`.

-->

## Resources

+ <https://python-markdown.github.io/>
+ <https://python-markdown.github.io/extensions/>
+ <https://squidfunk.github.io/mkdocs-material/>
+ <https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/>
