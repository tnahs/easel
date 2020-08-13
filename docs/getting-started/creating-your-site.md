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

Create a page directory and a `page.yaml` file:

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

title: my-site
favicon:
copyright: © 2020 My Full Name

page:
  width:

colors:
  accent-base:
  accent-light:

menu:
  width:
  align:
  header:
    label: my-site
    image:
      path:
      width:
      height:
  items:
    - type: link-page
      label: my-page
      links-to: my-page
```

Note that under `menu:items` we have a single item with the attribute `links-to` set to `my-page`. This is a path relative to the `pages` directory referring to the `my-page` directory. Note that `links-to` always requires a path relative to the `pages` directory.

## Configuring the `page.yaml`

!!! info

    Each page directory requires a `page.yaml` file. In the way that `site.yaml` configures the site, `page.yaml` configures the page.

For this page we will do the laziest thing possible, create a `Lazy` page. This particular type of page auto-populates its contents from the contents of its respective folder sorted alphabetically by the absolute path of each item.

Add the following to the `page.yaml` file:

``` yaml
# my-easel/my-site/my-page/page.yaml

# Specify this page is the 'landing' page.
is-landing: true

# Page type.
type: lazy

# Lazy Page options.
options:
  show-captions: true
```

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
