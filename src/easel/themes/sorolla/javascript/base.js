"use strict"

class ContentTools {
    /*
     * See static/css/page.css for structures.
     * --------------------------------------------------------------------- */

    constructor() {
        this.contentItems = document.querySelectorAll(".content__item")

        // TODO:LOW The above attributes are class-attributes. They are placed
        // inside the constructor for Safari support. Re-work when converting
        // to TypeScript.

        this.contentItems__toLazyLoad = [...this.contentItems].filter((item) =>
            item.hasAttribute("data-src")
        )

        this.contentItems__toWrapProxy = [...this.contentItems].filter((item) =>
            item.hasAttribute("data-proxy-color")
        )

        this.contentItems__toResizeEmbedded = document.querySelectorAll(
            ".content__item--embedded iframe"
        )
    }

    setup() {
        this._setupProxyColors()
        this._setupEmbeddedContentItems()
        this._setupObservers()
    }

    _setupProxyColors() {
        const documentStyle = getComputedStyle(document.documentElement)

        const proxyColorFallback = documentStyle.getPropertyValue(
            "--proxy-color--fallback"
        )

        const proxyAlpha = documentStyle.getPropertyValue(
            "--proxy-color--alpha"
        )

        this.contentItems__toWrapProxy.forEach((contentItem) => {
            const proxyColor = this._getProxyColor(
                contentItem,
                proxyAlpha,
                proxyColorFallback
            )

            this._wrapProxyColor(contentItem, proxyColor)
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

                setTimeout(() => {
                    this._triggerFadeIn(entry.target)
                }, 500)

                observer.unobserve(entry.target)
            })
        }

        const fadeInOptions = {
            root: null, // Entire viewport
            rootMargin: "0px 0px 0px 0px",
            threshold: 0, // Trigger immediately on viewport enter
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
            threshold: 0, // Trigger immediately on viewport enter
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

    // Proxy Color methods

    _getProxyColor(element, proxyAlpha, proxyColorFallback) {
        let color

        try {
            color = JSON.parse(element.dataset.proxyColor)
        } catch {
            return proxyColorFallback
        }

        // Check that color object has "R", "G" and "B" keys.
        if (!("R" in color) || !("G" in color) || !("B" in color)) {
            return proxyColorFallback
        }

        return `rgba(${color.R}, ${color.G}, ${color.B}, ${proxyAlpha})`
    }

    _wrapProxyColor(element, proxyColor) {
        const wrapper = document.createElement("div")

        element.parentNode.insertBefore(wrapper, element)

        wrapper.classList.add("proxy-color-wrapper")
        wrapper.style.backgroundColor = proxyColor
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
