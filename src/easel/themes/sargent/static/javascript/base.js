"use strict"

class ContentTools {
    contentItems = document.querySelectorAll("[class^='content-item__']")

    constructor() {
        this.contentItems__toLazyLoad = [...this.contentItems].filter((item) =>
            item.hasAttribute("data-src")
        )

        this.contentItems__toWrapPlaceholder = [
            ...this.contentItems,
        ].filter((item) => item.hasAttribute("data-placeholder-color"))

        this.contentItems__toResizeEmbedded = document.querySelectorAll(
            ".content-item__embedded iframe"
        )
    }

    setup() {
        this._setupPlaceholderColors()
        this._setupEmbeddedContentItems()
        this._setupObservers()
    }

    _setupPlaceholderColors() {
        // TODO: Do we want to add another layer of fallback in case the CSS
        // properties aren't defined?

        const documentStyle = getComputedStyle(document.documentElement)

        const placeholderColorFallback = documentStyle.getPropertyValue(
            "--placeholder-color--fallback"
        )

        const placeholderAlpha = documentStyle.getPropertyValue(
            "--placeholder-color--alpha"
        )

        this.contentItems__toWrapPlaceholder.forEach((contentItem) => {
            const placeholderColor = this._getPlaceholderColor(
                contentItem,
                placeholderAlpha,
                placeholderColorFallback
            )

            this._wrapPlaceholderColor(contentItem, placeholderColor)
        })
    }

    _setupEmbeddedContentItems() {
        this.contentItems__toResizeEmbedded.forEach((contentItem) => {
            this._resizeEmbeddedContentItem(contentItem)
        })
    }

    _setupObservers() {
        const fadeInCallback = (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return
                }

                this._triggerFadeIn(entry.target)

                observer.unobserve(entry.target)
            })
        }

        const fadeInOptions = {
            root: null, // Entire viewport
            rootMargin: "0px 0px 0px 0px",
            threshold: 0.5, // Trigger when element is 50% visible
        }

        const lazyLoadCallback = (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return
                }

                this._triggerLazyLoad(entry.target)

                observer.unobserve(entry.target)
            })
        }

        const lazyLoadOptions = {
            root: null, // Entire viewport
            rootMargin: "0px 0px 25% 0px", // Trigger outside the viewport
            threshold: 0,
        }

        const fadeInObserver = new IntersectionObserver(
            fadeInCallback,
            fadeInOptions
        )

        const lazyLoadObserver = new IntersectionObserver(
            lazyLoadCallback,
            lazyLoadOptions
        )

        this.contentItems.forEach((contentItem) => {
            fadeInObserver.observe(contentItem)
        })

        this.contentItems__toLazyLoad.forEach((contentItem) => {
            lazyLoadObserver.observe(contentItem)
        })
    }

    // Placeholder Color methods

    _getPlaceholderColor(element, placeholderAlpha, placeholderColorFallback) {
        let color

        try {
            color = JSON.parse(element.dataset.placeholderColor)
        } catch {
            return placeholderColorFallback
        }

        // Check that color object has "r", "g" and "b" keys.
        if (!("r" in color) || !("g" in color) || !("b" in color)) {
            return placeholderColorFallback
        }

        return `rgba(${color.r}, ${color.g}, ${color.b}, ${placeholderAlpha})`
    }

    _wrapPlaceholderColor(element, placeholderColor) {
        const wrapper = document.createElement("div")

        element.parentNode.insertBefore(wrapper, element)

        wrapper.classList.add("placeholder-color")
        wrapper.style.backgroundColor = placeholderColor
        wrapper.appendChild(element)
    }

    // Fade-in and LazyLoad methods

    _triggerFadeIn(element) {
        element.classList.add("animation__fade-in")
    }

    _triggerLazyLoad(element) {
        element.src = element.dataset.src
    }

    // Embedded Content Item methods

    _resizeEmbeddedContentItem(element) {
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
    const contentTools = new ContentTools()

    contentTools.setup()
})
