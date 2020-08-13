# Site

## General

`title`
:   Default: `null` -- The title of the site. Placed in the `<title>` tag.

`favicon`
:   Default: `null` -- A path to a favicon. This must be a path relative to the site directory i.e, the one containing the `site.yaml` file.

`copyright`
:   Default: `null` -- Copyright information to be displayed inside the `<footer>` tag.

## Page

`page.width`
:   Default: `800px` -- Width of the site not including the menu.

## Colors

`colors.accent-base`
:   Default: `hsla(25, 90%, 60%, 1.00)` -- Base accent color.

`colors.accent-light`
:   Default: `hsla(25, 100%, 85%, 1.00)` -- Donec convallis convallis tellus, id dictum metus porttitor at.

## Menu

`menu.width`
:   Default: `175px"` -- Sed eget porttitor enim, quis mattis tortor.

`menu.align`
:   Default: `left` -- Donec blandit leo eros, at tincidunt augue elementum id.

`menu.header.label`
:   Default: `null` -- Etiam porta rhoncus mi, vel vulputate ante placerat eu.

`menu.header.image.path`
:   Default: `null` -- Fusce quam justo, accumsan non vehicula a, aliquet eget metus.

`menu.header.image.width`
:   Default: `menu.width` -- Aenean eget erat nec libero dictum tempus bibendum ut turpis.

`menu.header.image.height`
:   Default: `auto` -- Fusce nec luctus nisi, non elementum ipsum.

`menu.items`
:   Default: `[]` -- Sed sagittis ipsum non tempus volutpat. See [Menu Item Types](#menu-item-types) for a list of available types.

### Menu Item Types

#### Shared Attributes

`type`
:   Sed sagittis ipsum non tempus volutpat.

:   Valid options are: `link-page` `link-url` `section` `spacer`

#### Link Page

`label`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

`links-to`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
menu:
  items:
    - type: link-page
      label: my-page
      links-to: my-page-directory
```

#### Link URL

`label`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

`url`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
menu:
  items:
    - type: link-url
      label: external-url
      url: www.external-url.com
```

#### Section

`label`
:   Default: `null` -- Sed sagittis ipsum non tempus volutpat.

``` yaml
menu:
  items:
    - type: section
      label: other-projects
```

#### Spacer

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
favicon:
copyright:

page:
  width:

colors:
  accent-base:
  accent-light:

menu:
  width:
  align:
  header:
    label:
    image:
      path:
      width:
      height:
  items:
```

## Blank Configuration

``` yaml
title:
favicon:
copyright:

page:
  width:

colors:
  accent-base:
  accent-light:

menu:
  width:
  align:
  header:
    label:
    image:
      path:
      width:
      height:
  items:
```
