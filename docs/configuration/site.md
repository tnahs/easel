# Site

## General

`title`
:   Default: `""` -- The title of the site. Placed in the `<title>` tag.

`author`
:   Default: `""` -- Sed sagittis ipsum non tempus volutpat.

`copyright`
:   Default: `""` -- Copyright information to be displayed inside the `<footer>` tag.

`favicon`
:   Default: `""` -- A path to a favicon. This must be a path relative to the site directory i.e, the one containing the `site.yaml` file.

## Menu

`menu`
:   Default: `[]` -- Sed sagittis ipsum non tempus volutpat. Aenean interdum bibendum nisi, at vulputate tellus euismod sed. Sed iaculis dui at vehicula mollis. Ut fringilla consequat nibh id tincidunt. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. See [Menu Item Types](#menu-item-types) for a list of available types.

## Theme

Sed sagittis ipsum non tempus volutpat. Aenean interdum bibendum nisi, at vulputate tellus euismod sed. Sed iaculis dui at vehicula mollis. Ut fringilla consequat nibh id tincidunt. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.

### Menu

`theme.menu.width`
:   Default: `175px` -- Sed eget porttitor enim, quis mattis tortor.

`theme.menu.align`
:   Default: `left` -- Donec blandit leo eros, at tincidunt augue elementum id.

`theme.menu.header.label`
:   Default: `null` -- Etiam porta rhoncus mi, vel vulputate ante placerat eu.

`theme.menu.header.image.path`
:   Default: `null` -- Fusce quam justo, accumsan non vehicula a, aliquet eget metus.

`theme.menu.header.image.width`
:   Default: `theme.menu.width` -- Aenean eget erat nec libero dictum tempus bibendum ut turpis.

`theme.menu.header.image.height`
:   Default: `auto` -- Fusce nec luctus nisi, non elementum ipsum.

### Page

`theme.page.width`
:   Default: `800px` -- Width of the site not including the menu.

`theme.page.align`
:   Default: `left` -- Width of the site not including the menu.

### Colors

`theme.colors.accent-base`
:   Default: `hsla(25, 90%, 60%, 1.00)` -- Base accent color.

`theme.colors.accent-light`
:   Default: `hsla(25, 100%, 85%, 1.00)` -- Donec convallis convallis tellus, id dictum metus left at.

## Menu Item Types

### Shared Attributes

`type`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat. Aenean interdum bibendum nisi, at vulputate tellus euismod sed. Sed iaculis dui at vehicula mollis. Ut fringilla consequat nibh id tincidunt.

:   Valid options are: `link-page` `link-url` `section` `spacer`

### Link Page

`label`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

`links-to`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
menu:
  items:
    - type: link-page
      label: my-page
      links-to: my-page-directory
```

### Link URL

`label`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

`url`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
menu:
  items:
    - type: link-url
      label: external-url
      url: www.external-url.com
```

### Section

`label`
:   Default: `null` -- Required -- Sed sagittis ipsum non tempus volutpat.

``` yaml
menu:
  items:
    - type: section
      label: other-projects
```

### Spacer

`size`
:   Default: `medium` -- Valid options are: `small`, `medium` or `large`.

``` yaml
menu:
  items:
    - type: spacer
      size: small
```

## Example Configuration

``` yaml
title:
author:
copyright:
favicon:

menu:
- type: link-page
  label:
  links-to:
- type: link-url
  label:
  url:
- type: section
  label:
- type: spacer
  size:

theme:
  menu:
    width:
    align:
    header:
      label: easel
      image:
        path:
        width:
        height:
  page:
    width:
    align:
  colors:
    accent-base:
    accent-light:

extras: {}
```
