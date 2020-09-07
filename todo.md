# TODOs

## HIGH

- Style 404
- Style Markdown
- Remove all `#ids` from styling.
- Use gulp to copy/install `reset.css`, `normalize.css` and `hammmer.js` on dev/build

## MEDIUM

- ImagePlaceholder > ImageProxies
  - Add support for 3 sizes: `small`, `medium`, `large`.
- Set theme/custom-theme through 'site.yaml'

## LOW

- Convert CSS -> SASS
- Convert Javascript -> Typescript
- ThemeConfig class.
- Check placeholder generation for all Easel supported filetypes.
- Change `.cache` folder to `assets`.
- Can we make all calls to `main.static` into `site.static`? Or a custom method to retrieve site assets e.g. `{{ site.config.favicon | url }}`
- Lightbox
  - Fix styling on both desktop and mobile.
  - Use hammer.js - <https://github.com/hammerjs/hammer.js>
  - Documentation
  - Ignore pinch/zoom when open.
- Site ass Flask app.
  - On Easel.run()
    - Placeholders are generated and placed in site-name/assets/placeholders in the same way it's currently done. However let's remove the 'pages' folder and just place the individual page directories instead.
    - ...
- Site as flattened html -> `easel build`
  - On 'easel build'
    - ...

## QUESTIONS

## HOUSEKEEPING

- Documentation
- Print site map method.
- Unified validation setup.
- Sift through paths and URLs.

## FEATURES

- 'Collection' Page (For relating other pages or a blog.)
  - A child of a 'Collection' Page would maintain a link to it's siblings allowing navigation between them.
- 'Landing' Page
- 'Grid' that holds Content types
- CLI Tools: <https://click.palletsprojects.com/en/7.x/>
- Better way to find dominant/average color of an image.
- Menu item icon
- Custom Themes
  - Theme configuration file `theme.yaml` for theme development.
  - READ: <https://www.mkdocs.org/user-guide/custom-themes/>
  - READ: <https://www.mkdocs.org/user-guide/custom-themes/#packaging-themes>
  - Repo for 'easel-basic-theme'

## MISC

- Design Easel logo/icon.
- Themes Inspiration
  - <https://gates-demo.squarespace.com/>
  - <https://beaumont-demo.squarespace.com/>
  - <https://zion-demo.squarespace.com/>
  - <https://talva-demo.squarespace.com/?nochrome=true>

## DOCUMENTATION NOTES

- Galleries don't show captions on the page but rather in the lightbox view.

- Theme structure. All files and directories are copied to the Site directory except hidden folder i.e. `.images` which might hold source images unnecessary for rendering the theme.

    ``` plaintext
    theme
    ├── css
    ├── javascript
    ├── images
    ├── fonts
    ├── templates
    │   ├── 404.jinja
    │   └── main.jinja2
    └── .images
    ```

- Site structure when running as a Flask application:

    ``` plaintext
    site-name
    ├── site.yaml
    ├── pages
    │   ├── page01
    │   │   └── image001.jpg
    │   └── page02
    │       └──...
    └── assets
        ├── placeholders
        │   ├── page01
        │   │   └── image001
        │   │       ├── image.jpg
        │   │       └── color.json
        │   ├── page02
        │   │   └──...
        │   └──...
        └──...
    ```
