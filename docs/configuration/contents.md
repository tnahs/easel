# Contents

## Image

``` yaml
contents:
  - type: image
    path: # [path: null]
    caption:
      title: # [str: null]
      description: # [str: null]
```

## Video

``` yaml
contents:
  - type: video
    path: # [path: null]
    caption:
      title: # [str: null]
      description: # [str: null]
```

## Audio

``` yaml
contents:
  - type: audio
    path: # [path: null]
    caption:
      title: # [str: null]
      description: # [str: null]
```

## Embedded

``` yaml
contents:
  - type: embedded
    html: # [str: null]
    caption:
      title: # [str: null]
      description: # [str: null]
```

## TextBlock

``` yaml
contents:
  - type: text-block
    path: # [path: null]
```

## Header

``` yaml
contents:
  - type: header
    body: # [str: null]
    size: # [str: "medium"] ("small", "medium", "large")
```

## Break

``` yaml
contents:
  - type: break
    size: # [str: "medium"] ("small", "medium", "large")
```
