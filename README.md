# Easel

Showcasing work for the lazy. Built on Flask, YAML, Markdown and directories.

## Installation

### Create an environment

Create a project directory and a venv directory within:

``` shell
$ mkdir my-easel
$ cd my-easel
$ python3 -m venv venv
```

### Activate the environment

Before you work on your project, activate the corresponding environment:

``` shell
$ source venv/bin/activate
```

Your shell prompt will change to show the name of the activated environment.

### Install Easel
Within the activated environment, use the following command to install Easel:

``` shell
$ pip install easel
```

Easel is now installed.


## A Lazy Site

### Create a site

Create a site directory and a `site.yaml` file:

``` shell
$ mkdir my-site
$ cd my-site
$ touch site.yaml
```

Add the following to the `site.yaml` file:

``` yaml
# my-easel/my-site/site.yaml

title: my-easel
favicon:
year: 2020
name: My Name

page:
  width:

colors:
  accent-base:
  accent-light:

menu:
  width:
  align:
  header:
    label: my-easel
    image:
      path:
      width:
      height:
  items:
    - type: link-page
      label: my-page
      links-to: my-page
```

Every site requires a `site.yaml` in the site's root directory. It's used to configure general site attributes namely the menu. Note that none of the items require a value, however all the items **must** be present. For example, `menu:items` can be an empty list, Easel will render no menu in this case. However if `menu:items` is missing a `ConfigError` will be thrown.

Note that under `menu:items` we have a single item with the attribute `links-to` set to `my-page`. This is a path relative to the `pages` directory referring to the directory `my-page` we will be making shortly. Note that `links-to` always requires a path relative to the `pages` directory.

Our Easel directory should now look like this:

``` shell
my-easel
├── my-site
│   └── site.yaml
└── venv
```

### Create a page

Create a page directory and a `page.yaml` file:

``` shell
$ mkdir my-page
$ cd my-page
$ touch page.yaml
```


Add the following to the `page.yaml` file:

``` yaml
# my-easel/my-site/my-page/page.yaml
# Lazy Page

# Specify this page is the 'landing' page.
is-landing: true

# Page type.
type: lazy

# Lazy Page options.
options:
  show-captions: true
```

Each page directory **must** contain a `page.yaml` file. In the same way that `site.yaml` configures the site, `page.yaml` configures the page. For this page we will do the laziest thing possible, create a `Lazy` page. This particular type of page auto populates its contents from the contents of its respective folder sorted alphabetically by the absolute path of each item.

Our Easel directory should now look like this:

``` shell
my-easel
├── my-site
│   ├── site.yaml
│   └── pages
│       └── my-page
│           └── page.yaml
└── venv
```

Now make sure to add some content: images, videos etc to the `my-page` directory:

``` shell
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

## A Minimal Application

A minimal Easel application looks something like this:

``` python
from easel import Easel

easel = Easel("my-site")

if __name__ == "__main__":
    easel.run()
```
Note that `my-site` refers to the directory `my-site`. We're providing a relative path here, telling Easel that our site directory is in the same directory as our application.

Now save it as `run.py` in your `my-easel` directory next to your `my-site` directory.

Finally, our Easel directory should look like this:

``` shell
my-easel
├── run.py
├── my-site
│   ├── site.yaml
│   └── pages
│       ├── my-page
│       │   ├── page.yaml
│       │   ├── image-001.jpg
│       │   ├── image-002.jpg
│       │   └── ...
│       └── ...
└── venv
```

To run the application simply run the script.

``` shell
$ python run.py
 * Running on http://127.0.0.1:5000/
```

So what did that code do?

+ First we imported the Easel class. An instance of this class will hold our Flask application.
+ Next we create an instance of this class. The first argument is the path to the directory containing your site along with its config files, pages and contents.
+ Finally we place `easel.run()` in a guard statement so we can run a local development server when we directly run our script.

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production. For deployment options see [Flask Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment).


Now head over to http://127.0.0.1:5000/, and you should see your beautiful work greeting.


<!-- TODO: Create easel-demo and link here. -->


# API

## Custom Types

``` python
# Import Easel's Page, Menu and Content factories.
from easel.site.pages import page_factory
from easel.site.menus import menu_factory
from easel.site.contents import content_factory

# Import your custom types.
from .custom import CustomPage, CustomMenu, CustomContent

# Register your custom types.
page_factory.register_page_type("custom-page", CustomPage)
menu_factory.register_menu_type("custom-menu", CustomMenu)
content_factory.register_content_type("custom-content", CustomContent)
```

## Custom Assets (templates & static files)

``` python
easel = Easel(
    site="my-site",
    custom_assets="my-custom-assets",
)
```

The assets directory **must** follow the following structure.

``` shell
my-custom-assets
│
├── templates
│   ├── page.jinja2
│   └── ...
│
└── static
    ├── css
    ├── js
    ├── fonts
    └── images

```
Additionally it must contain a `page.jinja2` template in the `templates` directory. This is the entry-point for rendering pages. See `easel.main.views.render_page` and `easel.main.views.page_landing`.


# Links / Resources

+ Releases: https://pypi.org/project/easel/
+ Flask documentation: https://github.com/pallets/flask