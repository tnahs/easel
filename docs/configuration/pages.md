# Page Types

## Shared Attributes

`type`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

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

### Content Types

#### Shared Attributes

`type`
:   Sed sagittis ipsum non tempus volutpat.

:   Valid options are: `image` `video` `audio` `embedded` `text-block` `header` `break`

`caption.title`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

`caption.description`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
caption:
  title: "Title"
  description: "Description"
```

#### Image

`path`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: image
    path:
```

#### Video

`path`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: video
    path:
```

#### Audio

`path`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: audio
    path:
```

#### Embedded

`html`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: embedded
    html:
```

#### Text Block

`path`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: text-block
    path:
```

#### Header

`body`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

`size`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: header
    body:
    size:
```

## Break

`size`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
contents:
  - type: break
    size:
```

## Markdown Page

Markdown Page Configuration

``` yaml
type: markdown
```
