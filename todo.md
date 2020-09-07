# TODOs

## HIGH

- Style 404 Page
- Style Markdown
- Setup `gulp` to:
  - Copy/install `reset.css`, `normalize.css` and `hammmer.js` on dev/build
  - Autoprefix with: `gulp-autoprefixer`
  - Minify CSS/JS
- Custom method to retrieve different assets e.g.:
  - `{{ theme.menu_button | url_theme }}`
  - `{{ site.config.favicon | url_site }}`

## MEDIUM

- ImagePlaceholder > ImageProxies
  - Add support for 3 sizes: `small`, `medium`, `large`.

## LOW

- Optimize fonts.
- ThemeConfig class.
- Convert CSS -> SASS
- Convert Javascript -> Typescript
- Change `.cache` folder to `assets`.
- Lightbox
  - Use `hammer.js` - <https://github.com/hammerjs/hammer.js>
  - Fix styling on both desktop and mobile.
  - Documentation
- Set theme/custom-theme through `site.yaml`
- Site ass `Flask` app.
  - Placeholders are generated and placed in site-name/assets/placeholders in the same way it's currently done. However let's remove the 'pages' folder and just place the individual page directories instead.
  - ...
- Site as flattened html -> `easel build`
  - ...

## QUESTIONS

## HOUSEKEEPING

- Documentation
- Print site map method.
- Unified validation setup.
- Sift through paths and URLs.
- CSS variable naming convention needs some work.
- Check placeholder generation for all Easel supported filetypes.

## FEATURES

- 'Collection' Page (For relating other pages or a blog.)
  - A child of a 'Collection' Page would maintain a link to it's siblings allowing navigation between them.
- 'Landing' Page
- 'Grid' that holds Content types
- CLI Tools: <https://click.palletsprojects.com/en/7.x/>
- Better way to find dominant/average color of an image.
- Menu item icon
- Custom Themes
  - READ: <https://www.mkdocs.org/user-guide/custom-themes/>
  - READ: <https://www.mkdocs.org/user-guide/custom-themes/#packaging-themes>
  - Theme configuration file `theme.yaml` for theme development.
  - Repo for 'easel-basic-theme'

## MISC

- Design Easel logo/icon.
- Themes Inspiration
  - <https://gates-demo.squarespace.com/>
  - <https://beaumont-demo.squarespace.com/>
  - <https://zion-demo.squarespace.com/>
  - <https://talva-demo.squarespace.com/?nochrome=true>
- Different name?
  - canvas
  - beacon
  - torch
  - pigment
  - mural
  - vitrine

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
