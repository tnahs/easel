# Custom assets

``` python
easel = Easel(
    site="my-site",
    custom_assets="my-custom-assets",
)
```

The assets directory **must** follow the following structure.

``` plaintext
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
