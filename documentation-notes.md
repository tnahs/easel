# Documentation Notes

- `Easel` refers to the Flask application that manages and runs the `Site` with its `Theme`.
- `Site` refers to all the content that belongs to the user. It contains the `Menu`, `Pages` and page `Contents`
- `Theme` refers to all the assets that is used to render the `Site`. This can be found in the site's directory if a custom theme is provided.
- Easel ignores files starting with `.` and `_`.
- Galleries don't show captions on the page but rather in the lightbox view.

## Theme Structure

Minimum requirements.

``` plaintext
.
├── 404.html
├── main.html
└── theme.yaml
```

Expanded example.

``` plaintext
.
├── static
│   ├── css
│   ├── javascript
│   ├── images
│   └── fonts
├── 404.html
├── base.html
├── main.html
└── theme.yaml
```

## Site Structure

Site structure when running as a Flask application:

``` plaintext
.
├── contents
│   ├── site.yaml
│   └── pages
│       ├── page01
│       │   └── image001.jpg
│       └── page02
│           └──...
└── site-assets
    ├── pages
    │   ├── page01
    │   │   └── image001-proxies
    │   │       ├── small.jpg
    │   │       ├── medium.jpg
    │   │       ├── large.jpg
    │   │       ├── average.json
    │   │       └── dominant.json
    │   ├── page02
    │   │   └──...
    │   └──...
    └──...
```

Site structure when running as a static site:

``` plaintext
build
├── index.html
├── 404.html
├── page01
│   └── index.html
├── page02
│   └── index.html
└── static
    ├── pages
    │   ├── page01
    │   │   ├── image001.jpg
    │   │   └── image001-proxies
    │   │       ├── small.jpg
    │   │       ├── medium.jpg
    │   │       └── large.jpg
    │   ├── page02
    │   │   └──...
    │   └──...
    └──...
```

## Creating an Easel instance

Setting site-root as environment variable.

``` console
$ export SITE_ROOT=./my-project
```

``` python
from easel import Easel

easel = Easel()
easel.run()
```

Setting site-root in Python.

``` python
from easel import Easel

easel = Easel("./my-project")
easel.run()
```

Implying the site-root is the current directory.

``` python
from easel import Easel

easel = Easel()
easel.run()
```

## Using the CLI

### Serving a site

Setting site-root as environment variable.

``` console
$ export SITE_ROOT=./my-project
$ easel serve
```

Setting site-root in as an optional argument.

``` console
$ easel --site-root=./my-project serve
```

Implying the site-root is the current directory.

``` console
$ easel serve
```

### Re-building the site-cache

Setting site-root as environment variable.

``` console
$ export SITE_ROOT=./my-project
$ easel rebuild-site-cache
```

Setting site-root in as an optional argument.

``` console
$ easel --site-root=./my-project rebuild-site-cache
```

Implying the site-root is the current directory.

``` console
$ easel rebuild-site-cache
```

## Setting a Theme

Using a build-in theme.

``` yaml
# site.yaml

# ...

theme:
  name: sorolla
```

Using an installed theme.

Note: All installed themes start with `easel-`.

``` yaml
# site.yaml

# ...

theme:
  name: easel-[theme-name]
```

Using an custom theme.

The value for `custom-path` is relative to the site-root i.e. the directory that contains the `site.yaml`

``` yaml
# site.yaml

# ...

theme:
  custom-path: ./custom-theme
```

Note: If both `theme.custom-path` and `theme.name` are set, `theme.custom-path` will always trump `theme.name`. A warning will be logged as well.

Note: The precedence order for setting a theme is: Custom > Installed > Built-in > Default i.e setting a custom theme trumps both setting an installed theme and setting an installed theme only trumps setting a built-in theme etc.

## Accessing Theme and Site configuration in Templates

``` jinja
{{ config.site }}
    {{ config.site.title }}
    {{ config.site.author }}
    {# ... #}

{{ config.theme }}
    {# ... #}

{{ index }}
    {{ index.url }}

{{ menu }}
{{ pages }}
```

## Site API

``` plaintext
Globals
│
├── .site_paths   :: SitePaths
├── .site_config  :: SiteConfig ───────┐
├── .theme_paths  :: ThemePaths        │
└── .theme_config :: ThemeConfig       │
                                       │
Easel                                  │
│                                      │
└── .site :: Site                      │
    │                                  │
    ├── .config :: Globals.SiteConfig ─┘
    │
    ├── .menu :: List[MenuType]
    │            ┌          ┐
    │            │ LinkPage │
    │            │ LinkURL  │
    │            │ Spacer   │
    │            └          ┘
    │
    └── .pages :: List[PageType]
        │         ┌               ┐
        │         │ Lazy          │
        │         │ Layout        │
        │         │ LazyGallery   │
        │         │ LayoutGallery │
        │         └               ┘
        │
        └── .contents :: List[ContentType]
                         ┌                                        ┐
                         │ Image                                  │
                         │ ├── .proxy_images :: ProxyImageManager │
                         │ │   ├── .small    :: ProxyImage        │
                         │ │   ├── .medium   :: ProxyImage        │
                         │ │   └── .large    :: ProxyImage        │
                         │ └── .proxy_colors :: ProxyColorManager │
                         │     ├── .average  :: ProxyColor        │
                         │     └── .dominant :: ProxyColor        │
                         │ Video                                  │
                         │ Audio                                  │
                         │ TextBlock                              │
                         │ Embedded                               │
                         │ Header                                 │
                         │ Break                                  │
                         └                                        ┘
```
