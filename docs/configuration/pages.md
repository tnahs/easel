# Page Types

## Shared Attributes

`is-index`
:   Default: `false` -- One page *must* have the `is-index` attribute set to true. This defines which page is shown when a visitor accesses the site i.e. `www.site.com` as opposed to `www.site.com/page`

    ``` yaml
    is-index: false
    ```

`type`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

:   Valid options are: `lazy` `lazy-gallery` `layout` `layout-gallery`

`options.show-captions`
:   Default: `false` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      show-captions: false
    ```

`options.column-count`
:   Default: `auto` -- Sed sagittis ipsum non tempus volutpat.

    ``` yaml
    options:
      column-count: auto
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
contents: []
```

`contents`
:   Default: `[]` -- Sed sagittis ipsum non tempus volutpat. See [Content Types](#content-types) for a list of available types.

## Lazy Gallery Page

Lazy Page Configuration

``` yaml
type: lazy-gallery
```

## Layout Gallery Page

Layout Page Configuration

``` yaml
type: layout-gallery
contents: []
```

`contents`
:   Default: `[]` -- Sed sagittis ipsum non tempus volutpat. See [Content Types](#content-types) for a list of available types.

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
  show-captions: true
```

Lazy Gallery Page Configuration

``` yaml
type: lazy-gallery

options:
  show-captions: true
  column-count: auto
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
  show-captions: true
```

Layout Gallery Page Configuration

``` yaml
type: layout-gallery

contents:
 - type: image
   path: image-01.png
   caption:
     title: Caption title.
     description: Caption description.

 - type: image
   path: image-02.png
   caption:
     title: Caption title.
     description: Caption description.

 - type: image
   path: image-03.png
   caption:
     title: Caption title.
     description: Caption description.


options:
  show-captions: true
  column-count: auto
```
