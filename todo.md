# TODOs

## HIGH

- Proxy image and proxy colors need re-working.
- Flatten unnecessarily nested SCSS styles.

## MEDIUM

- Complete `testing-demo` site.
- Implement a way to set Page's `column-count`.

## LOW

- Implement `MenuConfig` and `ContentConfig` types.
- Review and document paths in markdown files.
- Display a `Loading...` indicator when site-cache is being created.
- Reload `site.yaml` when the file is changed/saved.

## THEME:SOROLLA

## NEXT VERSION

- Build method to create flat HTML site.
- Move away from Flask.
  - Serve the `build` folder.
  - Try `watchdog`
  - Live-reloading
- Lossless image compression?
  - PIL `image.save("optimized-image.jpg", "JPEG", optimize=True, quality=85)`
    - `full.jpg`
    - `full-optimized.jpg` <- Use with a toggle in the `site.yaml`.
    - `small.jpg`
    - `medium.jpg`
    - `large.jpg`

## QUESTIONS

- Maybe all `ContentItems` have a `Proxy` element and each on is implemented differently?

## HOUSEKEEPING

- CSS variable naming convention needs some work.
- Check proxy image generation for all Easel supported filetypes.
- Sift through paths and URLs.
  - The way `Page` objects are referenced and identified is not very well documented. The same goes for `FileContent` objects
- Document Lightbox
- Import module? or import contents?
    `from . import errors` or `from .errors import Error`
- Square up SitePaths.root and SitePaths.static. Its a bit confusing.
- Unified validation setup.
- Documentation for using:
  - <https://www.netlify.com/>
  - <https://pages.github.com/>

## FEATURES

- More CLI Tools:
  - READ: <https://jekyllrb.com/docs/usage/>
- 'Collection' Page (For relating other pages or a blog.)
  - A child of a 'Collection' Page would maintain a link to it's siblings allowing navigation between them.
- 'Landing' Page
- 'Grid' that holds Content types
- Better way to find dominant/average color of an image.
- Repo for 'easel-basic-theme'
- Menu item icon
- Print site-map method.
