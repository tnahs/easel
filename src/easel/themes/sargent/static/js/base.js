"use strict"

class PageContentTools {
    constructor() {
        this.DEFAULT_PLACEHOLDER_COLOR = "red" //"rgba(0, 0, 0, .05)"
        this.PLACEHOLDER_COLOR_ALPHA = "0.75"

        this._contentItems = document.querySelectorAll(
            "[class^='content-item__']"
        )

        this._embeddedItems = document.querySelectorAll(
            ".content-item__embedded iframe"
        )

        const callback = (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return
                }

                if (!entry.intersectionRatio > 0) {
                    return
                }

                this._fadeInElement(entry.target)
                this._loadElement(entry.target)

                observer.unobserve(entry.target)
            })
        }

        this._intersectionObserver = new IntersectionObserver(callback, {
            rootMargin: "0px 0px -20% 0px",
        })
    }

    setup() {
        this._contentItems.forEach((contentItem) => {
            const placeholderColor = this._getPlaceholderColor(contentItem)
            this._wrapElement(contentItem, placeholderColor)

            this._intersectionObserver.observe(contentItem)
        })

        this._embeddedItems.forEach((embeddedItem) => {
            this._resizeEmbeddedItem(embeddedItem)
        })
    }

    _getPlaceholderColor(item) {
        let placeholderColor

        try {
            placeholderColor = JSON.parse(item.dataset.placeholderColor)
        } catch {
            placeholderColor = this.DEFAULT_PLACEHOLDER_COLOR
        }

        if (!placeholderColor.length) {
            placeholderColor = this.DEFAULT_PLACEHOLDER_COLOR
        } else {
            placeholderColor = `
                rgba(
                    ${placeholderColor[0]},
                    ${placeholderColor[1]},
                    ${placeholderColor[2]},
                    ${this.PLACEHOLDER_COLOR_ALPHA}
                    )
                `
        }
        return placeholderColor
    }

    _wrapElement(element, placeholderColor) {
        const wrapper = document.createElement("div")

        element.parentNode.insertBefore(wrapper, element)

        wrapper.classList.add("content__placeholder")
        wrapper.style.backgroundColor = placeholderColor
        wrapper.appendChild(element)
    }

    _fadeInElement(element) {
        element.classList.add("animation__fade-in")
    }

    _loadElement(element) {
        if (element.dataset.src === undefined) {
            return
        }

        element.src = element.dataset.src
    }

    _resizeEmbeddedItem(element) {
        /**
         * Some elements might have a 'height' and 'width' property defined in
         * the iframe tag. If that's the case, generate the ratio from these
         * values, otherwise fallback on using scrollHeight/scrollWidth.
         */

        const _sizeRatio = element.height / element.width
        const _sizeRatioScroll = element.scrollHeight / element.scrollWidth

        const sizeRatio = (_sizeRatio || _sizeRatioScroll || 0) * 100

        if (!sizeRatio) {
            return
        }

        element.parentElement.style.width = "100%"
        element.parentElement.style.position = "relative"
        element.parentElement.style.paddingBottom = `${sizeRatio}%`

        element.style.top = "0"
        element.style.left = "0"
        element.style.width = "100%"
        element.style.height = "100%"
        element.style.position = "absolute"
    }
}

window.addEventListener("load", () => {
    const pageContentTools = new PageContentTools()

    pageContentTools.setup()
})
