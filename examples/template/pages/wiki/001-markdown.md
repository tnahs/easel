## Using Markdown

### Basic Formatting

Emphasis, aka italics, with *asterisks*.

Underlines with _underscores_.

Strong emphasis, aka bold, with **asterisks** or __double underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

Highlight uses two equals signs. ==Highlight this.==

<br>

``` markdown
Emphasis, aka italics, with *asterisks*.

Underlines with _underscores_.

Strong emphasis, aka bold, with **asterisks** or __double underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

Highlight uses two equals signs. ==Highlight this.==
```

***

### Lists

1. First ordered list item
2. Another item
  * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
  1. Ordered sub-list
4. And another item.

  You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown). You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

<br>

* Unordered list can use asterisks
- Or minuses
  - Unordered sub-list.
  * Unordered sub-list.
+ Or pluses
  + Unordered sub-list.

<br>

``` markdown
1. First ordered list item
2. Another item
  * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
  1. Ordered sub-list
4. And another item.

  You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown). You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces (at least one, but we'll use three here to also align the raw Markdown).

<br>

* Unordered list can use asterisks
- Or minuses
  - Unordered sub-list.
  * Unordered sub-list.
+ Or pluses
  + Unordered sub-list.
```



***

[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with a tool-tip title](https://www.google.com "Google's Homepage")

[I'm a relative link](../blob/master/LICENSE)

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself].

URLs and URLs in angle brackets will automatically get turned into links.
http://www.example.com or <http://www.example.com> and sometimes example.com.

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com

***

Inline code has `single` back-ticks around it.

Block code has three back-ticks around it.

``` python
def page_or_404(self, requested_page_url):
  for page in self._pages:
    if page.url == requested_page_url:
      return page
  return abort(404)
```

***

5^10^
5^10\ thousand^

Trademark(tm)

Task List

- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
- [ ] item 2
- [ ] item 3

***

> Blockquotes: Quibusdam ab nulla necessitatibus unde ipsa ratione veritatis explicabo, eum ea quaerat vitae, optio sint, fugiat atque exercitationem fugit? Pariatur odit repudiandae dignissimos hic iure incidunt dicta harum deleniti accusamus modi consectetur magnam amet ipsam suscipit consequuntur, itaque quis?
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.

***

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.

***

Footnotes[^1] are added in-text like so[^2] with a matching footnote definition at the end of the document:

Nunc eu mauris blandit, facilisis massa quis, condimentum nisi.[^@#$%] Aenean hendrerit eros eu est facilisis, hendrerit faucibus sapien facilisis. Donec malesuada tellus in accumsan placerat. Aenean sed dolor lacus. Etiam gravida consectetur turpis nec ultrices. Donec arcu sem, congue et viverra ac, tincidunt vel lectus. Aliquam vitae laoreet leo. Sed purus metus, convallis non fermentum at, suscipit vel felis. In congue est convallis consequat vestibulum. Sed a porttitor erat. Etiam nec leo vel diam bibendum sodales a eget purus. Sed venenatis ex id magna commodo, eu accumsan nunc eleifend. Morbi interdum, ligula at pulvinar pellentesque, ligula quam ullamcorper leo, quis vestibulum leo tortor ut odio. Maecenas elementum consequat purus, ut euismod justo aliquam a. Lorem ipsum dolor sit amet, consectetur adipiscing elit.

[^1]:
  The first paragraph of the definition. Pariatur odit repudiandae dignissimos hic iure incidunt dicta harum deleniti accusamus modi consectetur magnam amet ipsam suscipit consequuntur, itaque quis? Quibusdam ab nulla necessitatibus unde ipsa ratione veritatis explicabo, eum ea quaerat vitae, optio sint, fugiat atque exercitationem fugit? Pariatur odit repudiandae dignissimos hic iure incidunt dicta harum deleniti accusamus modi consectetur magnam amet ipsam suscipit consequuntur, itaque quis?


[^@#$%]:
  A footnote on the label: "@#$%".


[^2]:
  Footnotes are the mind killer.
  Footnotes are the little-death that brings total obliteration.
  I will face my footnotes.