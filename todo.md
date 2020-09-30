# TODOs

## HIGH

- Proxy image and proxy colors need re-working.
- Maybe all `ContentItems` have a `Proxy` element and each on is implemented differently?
- Style and set content for footers in `base.html` and `menu-mobile.html`

## MEDIUM

- Review and document how paths work in Markdown files.
- Re-work the way the `Site` object is being created and move away from Flask's `current_app`. Seeing as `Site` is only dependant on Globals, it can be instantiated anywhere. In fact maybe it should be bound to the `Globals` object.
- Standardize how we're using `*args` and `**kwargs` when creating `Pages`, `Menus` and `Contents`.

## LOW

- Display a `Loading...` indicator when site-cache is being created.
- Complete `testing-demo` site.
- Locale detection for date formatting.
- Redesign CLI so we can run `easel serve --site-root=./path --debug`

## THEME:SOROLLA

- Add `Page.date` to templates. When locale detection works.

## NEXT VERSION

- Build method to create flat HTML site.
- Move away from Flask.
  - Serve the `build` folder.
  - Try `watchdog`
  - Live-reloading
    - Reload `site.yaml` when the file is changed/saved.
- Lossless image compression?
  - PIL `image.save("optimized-image.jpg", "JPEG", optimize=True, quality=85)`
    - `full.jpg`
    - `full-optimized.jpg` <- Use with a toggle in the `site.yaml`.
    - `small.jpg`
    - `medium.jpg`
    - `large.jpg`

## QUESTIONS

- Should `{{ index.url }}` return `\`?
- Is it worth implementing `MenuConfig` and `ContentConfig` types?
- Is it worth/possible to decouple `Page` from `Contents`

## HOUSEKEEPING

- Check proxy image generation for all Easel supported filetypes.
- Sift through paths and URLs.
  - The way `Page` objects are referenced and identified is not very well documented. The same goes for `FileContent` objects
- Square up `SitePaths.root` and `SitePaths.static`. It's a bit confusing.
- Unified validation setup.
- Documentation for using:
  - <https://www.netlify.com/>
  - <https://pages.github.com/>
- Lineup naming: invalid/valid supported/unsupported
- Clean-up Error names.

## FEATURES

- More CLI Tools:
  - READ: <https://jekyllrb.com/docs/usage/>
- 'Collection' Page (For relating pages or a blog.)
  - A child of a 'Collection' Page would maintain a link to it's siblings and parent allowing navigation between them.
- 'Landing' Page
- 'Grid' that holds Content types
- Better way to find dominant color of an image.
- Repo for 'easel-basic-theme'
- Print site-map method.
