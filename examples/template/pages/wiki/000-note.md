This is `000-note.md`. When inserting images into a markdown page or a markdown content item all paths must be relative to the parent page folder. With a structure like this:

```
[site]
└── pages
    ├── [other-pages]
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

---

One page *must* have the `is-landing` attribute set to true. This defines which page is shown when a visitor accesses the site i.e. `www.site.com` as opposed to `www.site.com/page`