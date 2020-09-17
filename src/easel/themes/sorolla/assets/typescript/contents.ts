"use strict"

interface Color {
    R: number
    G: number
    B: number
}

class AllContentItems {
    private FADE_IN_CLASS = "animation--fade-in"
    private FADE_IN_DELAY = 500

    private items = document.querySelectorAll<HTMLElement>(".content__item")

    setup(): void {
        this.setupFadeInObserver()
    }

    private setupFadeInObserver(): void {
        const fadeInCallback = (
            entries: IntersectionObserverEntry[],
            observer: IntersectionObserver
        ) => {
            entries.forEach((entry: IntersectionObserverEntry) => {
                if (!entry.isIntersecting) {
                    return
                }

                setTimeout(() => {
                    this.triggerFadeIn(<HTMLElement>entry.target)
                }, this.FADE_IN_DELAY)

                observer.unobserve(entry.target)
            })
        }

        const fadeInObserver = new IntersectionObserver(fadeInCallback, {
            root: null, // Entire viewport
            rootMargin: "0px 0px 0px 0px",
            threshold: 0, // Trigger immediately on viewport enter
        })

        this.items.forEach((item) => {
            fadeInObserver.observe(item)
        })
    }

    private triggerFadeIn(element: HTMLElement): void {
        element.classList.add(this.FADE_IN_CLASS)
    }
}

class ImageContentItems {
    private items = document.querySelectorAll<HTMLImageElement>(
        ".content__item--image"
    )

    private items__toLazyLoad = [...this.items].filter((item) =>
        item.hasAttribute("data-src")
    )

    private items__toWrapWithProxyColor = [...this.items].filter((item) =>
        item.hasAttribute("data-proxy-color")
    )

    private style = getComputedStyle(document.documentElement)
    private proxyColorFallback = this.style.getPropertyValue(
        "--proxy-color--fallback"
    )
    private proxyAlpha = this.style.getPropertyValue("--proxy-color--alpha")

    setup(): void {
        this.setupProxyColors()
        this.setupLazyLoadObserver()
    }

    private setupProxyColors(): void {
        this.items__toWrapWithProxyColor.forEach((item) => {
            this.wrapWithProxyColor(item)
        })
    }

    private setupLazyLoadObserver(): void {
        const lazyLoadCallback = (
            entries: IntersectionObserverEntry[],
            observer: IntersectionObserver
        ) => {
            entries.forEach((entry: IntersectionObserverEntry) => {
                if (!entry.isIntersecting) {
                    return
                }

                this.triggerLazyLoad(<HTMLImageElement>entry.target)

                observer.unobserve(entry.target)
            })
        }

        const lazyLoadObserver = new IntersectionObserver(lazyLoadCallback, {
            root: null, // Entire viewport
            rootMargin: "0px 0px 25% 0px", // Trigger outside the viewport
            threshold: 0, // Trigger immediately on viewport enter
        })

        this.items__toLazyLoad.forEach((item) => {
            lazyLoadObserver.observe(item)
        })
    }

    private wrapWithProxyColor(element: HTMLElement): void {
        const proxyColor = this.getProxyColor(element)

        const wrapper = document.createElement("div")

        element.parentNode.insertBefore(wrapper, element)

        wrapper.classList.add("proxy-color-wrapper")
        wrapper.style.backgroundColor = proxyColor
        wrapper.appendChild(element)
    }

    private getProxyColor(element: HTMLElement): string {
        let color: Color

        try {
            color = JSON.parse(element.dataset.proxyColor)
        } catch {
            return this.proxyColorFallback
        }

        // Check that color object has "R", "G" and "B" keys.
        if (!("R" in color) || !("G" in color) || !("B" in color)) {
            return this.proxyColorFallback
        }

        return `rgba(${color.R}, ${color.G}, ${color.B}, ${this.proxyAlpha})`
    }

    private triggerLazyLoad(element: HTMLImageElement): void {
        element.src = element.dataset.src
    }
}

class EmbeddedContentItems {
    private items = document.querySelectorAll<HTMLElement>(
        ".content__item--embedded"
    )

    public setup(): void {
        this.items.forEach((contentItem) => {
            this.resizeEmbeddedContentItem(contentItem)
        })
    }

    private resizeEmbeddedContentItem(element: HTMLElement): void {
        /**
         * Some elements might have a 'height' and 'width' property defined in
         * the iframe tag. If that's the case, generate the ratio from these
         * values, otherwise fallback on using scrollHeight/scrollWidth.
         */

        const iframe = element.querySelector("iframe")

        if (iframe === null) {
            return
        }

        const sizeRatio_ = Number(iframe.height) / Number(iframe.width)
        const sizeRatioScroll_ = iframe.scrollHeight / iframe.scrollWidth

        const sizeRatio = (sizeRatio_ || sizeRatioScroll_ || 0) * 100

        if (!sizeRatio) {
            return
        }

        iframe.parentElement.style.width = "100%"
        iframe.parentElement.style.position = "relative"
        iframe.parentElement.style.paddingBottom = `${sizeRatio}%`

        iframe.style.top = "0"
        iframe.style.left = "0"
        iframe.style.width = "100%"
        iframe.style.height = "100%"
        iframe.style.position = "absolute"
    }
}

window.addEventListener("load", () => {
    new AllContentItems().setup()
    new ImageContentItems().setup()
    new EmbeddedContentItems().setup()
})
