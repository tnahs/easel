# Custom Themes

``` plaintext
my-custom-theme
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

Additionally it must contain a `page.jinja2` template in the `templates` directory. This is the entry-point for rendering pages. See `easel.main.views.render_page` and `easel.main.views.index`.
