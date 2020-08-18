# A Minimal Application

A minimal Easel application looks something like this:

``` python
from easel import Easel


easel = Easel("my-site")


if __name__ == "__main__":

    easel.run()
```

!!! info

    Note that `my-site` refers to the directory `my-site`. We're providing a relative path here, telling Easel that our site directory is in the same directory as our application.

Now save it as `run.py` in your `my-easel` directory next to your `my-site` directory.

Finally, our Easel directory should look like this:

``` plaintext
my-easel
├── run.py
├── my-site
│   ├── site.yaml
│   └── pages
│       ├── my-page
│       │   ├── page.yaml
│       │   ├── description.md
│       │   ├── image-001.jpg
│       │   ├── image-002.jpg
│       │   └── ... Additional Content
│       └── ... Additional Pages
└── venv
```

To run the application simply run the script.

``` console
$ python run.py
 * Running on http://127.0.0.1:5000/
```

!!! question "So what did that code do?"

    - First we imported the Easel class. An instance of this class returns a thinly wrapped Flask application.
    - Next we create an instance of this class. The first argument is the path to the directory containing your site along with its config files, pages and contents.
    - Finally we place `easel.run()` in a guard statement so we can run the local development server only when our script is run from command-line.

This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production. For deployment options see [Flask Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment).

Now head over to <http://127.0.0.1:5000/>, and you should see your beautiful work.
