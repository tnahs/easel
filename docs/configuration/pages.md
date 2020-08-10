# Pages

One page *must* have the `is-landing` attribute set to true. This defines which page is shown when a visitor accesses the site i.e. `www.site.com` as opposed to `www.site.com/page`

## Lazy Page

Lazy Page Configuration

``` yaml
type: lazy

options:
  is-gallery: # [bool: false]
  gallery-column-count: # [int|str: "auto"]
  gallery-column-width: # [str: "250px"]
  show-captions: # [bool: false]

```

## Layout Page

Layout Page Configuration

``` yaml
type: layout

options:
  is-gallery: # [bool: false]
  gallery-column-count: # [int|str: "auto"]
  gallery-column-width: # [str: "250px"]
  show-captions: # [bool: false]

contents:
  # [list<ContentTypes>: null]
```

See [Contents](contents.md) for a list of available types.

## Markdown Page

Markdown Page Configuration

``` yaml
type: markdown

options:
  is-gallery: # [bool: false]
  gallery-column-count: # [int|str: "auto"]
  gallery-column-width: # [str: "250px"]
```

### Inserting Images

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
