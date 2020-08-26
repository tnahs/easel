# Creating Your Site

## Building the Scaffold

Inside your project directory create an site directory and a `site.yaml` file:

``` console
$ mkdir my-site
$ cd my-site
$ touch site.yaml
```

Our project directory should now look like this:

``` plaintext
my-easel
├── my-site
│   └── site.yaml
└── venv
```

Create a page directory and its `page.yaml` file:

``` console
$ mkdir pages
$ cd pages
$ mkdir my-page
$ cd my-page
$ touch page.yaml
```

Our project directory should now look like this:

``` plaintext
my-easel
├── my-site
│   ├── site.yaml
│   └── pages
│       └── my-page
│           └── page.yaml
└── venv
```

## Configuring the `site.yaml`

!!! info

    Every site requires a `site.yaml` in the site's root directory. It's used to configure general site attributes as well as the menu.

Add the following to the `site.yaml` file:

``` yaml
# my-easel/my-site/site.yaml

title: easel
author: My Full Name
copyright: © 2020 My Full Name
favicon:

menu:
- type: link-page
  label: my-page
  links-to: my-page

theme:
  menu:
    width:
    align:
    header:
      label: easel
      image:
        path:
        width:
        height:
  page:
    width:
    align:
  colors:
    accent-base:
    accent-light:
```

Note that under `menu` we have a single item with the attribute `links-to` set to `my-page`. This is a path relative to the `pages` directory referring to the `my-page` directory we just created.

## Configuring the `page.yaml`

!!! info

    Each page directory requires a `page.yaml` file. In the way that `site.yaml` configures the site, `page.yaml` configures the page. If no `page.yaml` file is detected, the directory will be ignored.

For this page we will do the laziest thing possible, create a `Lazy` page. This particular type of page auto-populates its contents from the contents of its respective directory sorted alphabetically by the absolute path of each item.

Add the following to the `page.yaml` file:

``` yaml
# my-easel/my-site/pages/my-page/page.yaml

is-index: true

type: lazy

options:
  show-captions: true
```

`is-index`
:   Defines which page will be the index page for the site i.e. `www.site.com` as opposed to `www.site.com/page`. Seeing as we only have one page in our site, it must be the index page.

!!! warning

    Every site must have one and only one page defined as the index page. A `SiteConfigError` will be thrown if no page or more than one page has `is-index` set to `true`.

`type`
:   Defines the type of page. In this case, `lazy`.

`options.show-caption`
:   Enables (lazy) captions. On a `Lazy` page, captions are generated from the filename (minus the file extension) of each item that supports captions.

## Adding Some Content

Now make sure to add some content: images, videos etc to the `my-page` directory:

``` plaintext
my-easel
├── my-site
│   ├── site.yaml
│   └── pages
│       └── my-page
│           ├── page.yaml
│           ├── image-01.jpg
│           ├── image-02.jpg
│           ├── video.mp4
│           └── ...
└── venv
```

Et voilà! Your site is ready almost for deployment!
