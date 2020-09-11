# TODOs

## HIGH

- ImagePlaceholder > ImageProxies
  - Add support for 3 sizes: `small`, `medium`, `large`.
- Change `.cache` folder to `assets`.
- Revisit how theme and site config values are accessed in the template.
- Better handling of non-existent 'page' objects in the template. This typically occurs when a 404 error occurs.

## MEDIUM

- Style 404 Page
- Style Page Description
- Style Markdown
- Setup `gulp` to:
  - Copy/install `reset.css`, `normalize.css` and `hammer.js` on dev/build
  - Autoprefix with: `gulp-autoprefixer`
  - Minify CSS/JS
- Optimize fonts.
- Fix Lightbox styling on both desktop and mobile.
- Need different values for IntersectionalObserver when dealing with large images.
- Implement default-dictionary/updating with `Menu` and `Content` types.

## LOW

- Convert CSS -> SASS
- Convert Javascript -> Typescript
- Use `hammer.js` - <https://github.com/hammerjs/hammer.js>
- Site as a `Flask` app.
  - Placeholders are generated and placed in site-name/assets/placeholders in the same way it's currently done. However let's remove the 'pages' folder and just place the individual page directories instead.
  - ...
- Site as a static site -> `easel build`
  - ...
- Rename `site` to ...? and `easel` to ...?

## QUESTIONS

## HOUSEKEEPING

- Document Lightbox
- Print site map method.
- Unified validation setup.
- Sift through paths and URLs.
- CSS variable naming convention needs some work.
- Check placeholder generation for all Easel supported filetypes.

## FEATURES

- CLI Tools: <https://click.palletsprojects.com/en/7.x/>
- 'Collection' Page (For relating other pages or a blog.)
  - A child of a 'Collection' Page would maintain a link to it's siblings allowing navigation between them.
- 'Landing' Page
- 'Grid' that holds Content types
- Better way to find dominant/average color of an image.
- Menu item icon
- Custom Themes
  - READ: <https://www.mkdocs.org/user-guide/custom-themes/>
  - READ: <https://www.mkdocs.org/user-guide/custom-themes/#packaging-themes>
  - Theme configuration file `theme.yaml` for theme development.
  - Repo for 'easel-basic-theme'

## Documentation Notes

- `Easel` refers to the Flask application that manages and runs the `Site` with it's `Theme`.
- `Site` refers to all the content that belongs to the user. It contains the `Menu`, `Pages` and page `Contents`
-`Theme` refers to all the content that is used to render the `Site`. This can be found in the site's directory if a custom theme is provided.

- Galleries don't show captions on the page but rather in the lightbox view.

### Theme Structure

Minimum requirements.

``` plaintext
.
├── static
├── templates
│   ├── 404.html
│   └── main.html
└── theme.yaml
```

Expanded example.

``` plaintext
.
├── static
│   ├── css
│   │   └── main.css
│   ├── javascript
│   │   └── main.js
│   ├── images
│   └── fonts
├── templates
│   ├── 404.html
│   ├── base.html
│   └── main.html
└── theme.yaml
```

### Site Structure

Site structure when running as a Flask application:

``` plaintext
.
├── site.yaml
├── pages
│   ├── page01
│   │   └── image001.jpg
│   └── page02
│       └──...
└── site-assets
    ├── pages
    │   ├── page01
    │   │   └── image001-proxies
    │   │       ├── small.jpg
    │   │       ├── medium.jpg
    │   │       ├── large.jpg
    │   │       └── color.json
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

### Creating an Easel instance

Setting site-root as environment variable.

``` console
$ export SITE_ROOT=./sorolla-demo
```

``` python
from easel import Easel

easel = Easel()
easel.run()
```

Setting site-root in Python.

``` python
from easel import Easel

easel = Easel("./sorolla-demo")
easel.run()
```

Implying the site-root is the current directory.

``` python
from easel import Easel

easel = Easel()
easel.run()
```

### Using the CLI

Setting site-root as environment variable.

``` console
$ export SITE_ROOT=./sorolla-demo
$ easel serve
```

Setting site-root in as an optional argument.

``` console
$ easel serve --site-root=./sorolla-demo
```

Implying the site-root is the current directory.

``` console
$ easel serve
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

## Accessing URLs in Templates

``` jinja
{{ site.index.url }}
{{ site.get_page('page-name').url }}
```
