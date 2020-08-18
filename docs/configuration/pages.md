# Page Types

## Shared Attributes

`type`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

`is-landing`
:   Default: `false` -- One page *must* have the `is-landing` attribute set to true. This defines which page is shown when a visitor accesses the site i.e. `www.site.com` as opposed to `www.site.com/page`

    ``` yaml
    is-landing: false
    ```

`options.is-gallery`
:   Default: `false` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      is-gallery: false
    ```

`options.gallery-column-count`
:   Default: `auto` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      gallery-column-count: auto
    ```

`options.gallery-column-width`
:   Default: `250px` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      gallery-column-width: 250px
    ```

`options.gallery-column-gap`
:   Default: `25px` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      gallery-column-gap: 25px
    ```

`options.show-captions`
:   Default: `false` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      show-captions: false
    ```

## Lazy Page

Lazy Page Configuration

``` yaml
type: lazy
```

## Layout Page

Layout Page Configuration

``` yaml
type: layout
contents:
```

`contents`
:   Default: `[]` -- Sed sagittis ipsum non tempus volutpat. See [Content Types](#content-types) for a list of available types.

## Markdown Page

Markdown Page Configuration

``` yaml
type: markdown
```

## Content Types

### Shared Attributes

`type`
:   Sed sagittis ipsum non tempus volutpat.

:   Valid options are: `image` `video` `audio` `embedded` `text-block` `header` `break`

`caption.title`
:   Default: `""` -- Sed sagittis ipsum non tempus volutpat.

`caption.description`
:   Default: `""` -- Sed sagittis ipsum non tempus volutpat.

`caption.align`
:   Default: `left` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
caption:
  title: Caption Title.
  description: Caption Description.
  align: left
```

### Image

`path`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: image
    path:
```

### Video

`path`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: video
    path:
```

### Audio

`path`
:   Default: `null`-- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: audio
    path:
```

### Embedded

`html`
:   Default: `null`-- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: embedded
    html:
```

### Text Block

`path`
:   Default: `null`-- Required -- Sed sagittis ipsum non tempus volutpat.

`align`
:   Default: `justify` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: text-block
    path: path/to/text-block.md
    align: justify
```

### Header

`text`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

`size`
:   Default: `medium` -- Sed sagittis ipsum non tempus volutpat.

`align`
:   Default: `left` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: header
    text: Header Text
    size: medium
    align: left
```

### Break

`size`
:   Default: `medium` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: break
    size: medium
```

## Example Configurations

Lazy Page Configuration

``` yaml
type: lazy

options:
  is-gallery: true
  gallery-column-count: auto
  gallery-column-width: 300px
  gallery-column-gap: 15px
  show-captions: true
```

Layout Page Configuration

``` yaml
type: layout

contents:
 - type: header
   text: My Page Header
   size: large

 - type: image
   path: image.png
   caption:
     title: Caption title.
     description: Caption description.

 - type: text-block
   path: my-blurb.md

options:
  is-gallery: true
  gallery-column-count: auto
  gallery-column-width: 300px
  gallery-column-gap: 15px
  show-captions: true
```

Markdown Page Configuration

``` yaml
type: markdown
```
