# TODOs

## HIGH

## MEDIUM

## LOW

- Implement `MenuConfig` and `ContentConfig` types.

## THEME:SOROLLA

- Style 404 Page
- Style Page Description
- Style Markdown
- Fix Lightbox styling on both desktop and mobile.
- Give each theme its own `gulpfile.js`
  - <https://macr.ae/article/splitting-gulpfile-multiple-files>
- Autoprefix CSS
- Minify CSS/JS
- Optimize fonts
- Convert CSS -> SASS
- Convert Javascript -> Typescript

## NEXT VERSION

- Build method to create flat HTML site.
- Move away from Flask.
  - Serve the `build` folder.
  - Try `watchdog`
  - Live-reloading
- Lossless image compression?

## QUESTIONS

## HOUSEKEEPING

- CSS variable naming convention needs some work.
- Check proxy image generation for all Easel supported filetypes.
- Sift through paths and URLs.
- Document Lightbox
- Import module? or import contents?
    `from . import errors` or `from .errors import Error`
- Square up SitePaths.root and SitePaths.static. Its a bit confusing.
- Unified validation setup.

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
