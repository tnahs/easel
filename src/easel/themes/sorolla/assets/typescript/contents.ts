type Color = {
    R: number
    G: number
    B: number
}

/*
 * See ./assets/scss/_contents.scss for structure.
 * ------------------------------------------------------------------------- */

class AllContentItems {
    readonly FADE_IN_CLASS = "animation--fade-in"
    readonly FADE_IN_DELAY = 500

    private items = document.querySelectorAll<HTMLDivElement>(".content__item")!

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
                    // TODO:LOW Is there a way to not have to re-cast this?
                    this.triggerFadeIn(<HTMLDivElement>entry.target)
                }, this.FADE_IN_DELAY)

                observer.unobserve(entry.target)
            })
        }

        const fadeInObserver = new IntersectionObserver(fadeInCallback, {
            root: null, // Observe entire viewport.
            rootMargin: "0px 0px 0px 0px", // Trigger inside the viewport.
            threshold: 0, // Trigger immediately on viewport enter.
        })

        this.items.forEach((item) => {
            fadeInObserver.observe(item)
        })
    }

    private triggerFadeIn(element: HTMLDivElement): void {
        element.classList.add(this.FADE_IN_CLASS)
    }
}

class ImageContentItems {
    private style = getComputedStyle(document.documentElement)
    readonly PROXY_COLOR_FALLBACK = this.style.getPropertyValue("--proxy-color--fallback")
    readonly PROXY_COLOR_ALPHA = this.style.getPropertyValue("--proxy-color--alpha")

    private items = document.querySelectorAll<HTMLImageElement>(".content__item--image")!

    setup(): void {
        this.setupProxyColors()
        this.setupLazyLoadImageObserver()
    }

    private setupProxyColors(): void {
        this.items.forEach((item) => {
            this.wrapWithProxyColor(item)
        })
    }

    private setupLazyLoadImageObserver(): void {
        const lazyLoadImageCallback = (
            entries: IntersectionObserverEntry[],
            observer: IntersectionObserver
        ) => {
            entries.forEach((entry: IntersectionObserverEntry) => {
                if (!entry.isIntersecting) {
                    return
                }

                // TODO:LOW Is there a way to not have to re-cast this?
                this.triggerLazyLoadImage(<HTMLImageElement>entry.target)

                observer.unobserve(entry.target)
            })
        }

        const lazyLoadImageObserver = new IntersectionObserver(lazyLoadImageCallback, {
            root: null, // Observe entire viewport.
            rootMargin: "0px 0px 25% 0px", // Trigger outside the viewport.
            threshold: 0, // Trigger immediately on viewport enter.
        })

        this.items.forEach((item) => {
            lazyLoadImageObserver.observe(item)
        })
    }

    private wrapWithProxyColor(element: HTMLImageElement): void {
        /* Wraps an image element with a div that contains the image's proxy
         * color as the background color.
         *
         * .content__container       --> .content__container
         *                           -->     .content__proxy-color-wrapper
         *     .content__item--image -->         .content__item--image
         */

        if (!element.hasAttribute("data-proxy-color")) {
            return
        }

        const wrapper = document.createElement("div")

        element.parentNode!.insertBefore(wrapper, element)

        wrapper.classList.add("content__proxy-color-wrapper")
        wrapper.style.backgroundColor = this.getProxyColor(element)
        wrapper.appendChild(element)
    }

    private getProxyColor(element: HTMLImageElement): string {
        if (!element.dataset.proxyColor) {
            return this.PROXY_COLOR_FALLBACK
        }

        let color: Color

        try {
            color = JSON.parse(element.dataset.proxyColor)
        } catch {
            return this.PROXY_COLOR_FALLBACK
        }

        // Check that color object has "R", "G" and "B" keys.
        if (!("R" in color) || !("G" in color) || !("B" in color)) {
            return this.PROXY_COLOR_FALLBACK
        }

        return `rgba(${color.R}, ${color.G}, ${color.B}, ${this.PROXY_COLOR_ALPHA})`
    }

    private triggerLazyLoadImage(element: HTMLImageElement): void {
        if (!element.dataset.src) {
            return
        }

        element.src = element.dataset.src
    }
}

class EmbeddedContentItems {
    private items = document.querySelectorAll<HTMLDivElement>(".content__item--embedded")

    public setup(): void {
        this.items.forEach((contentItem) => {
            this.resizeEmbeddedContentItem(contentItem)
        })
    }

    private resizeEmbeddedContentItem(element: HTMLDivElement): void {
        /**
         * Some elements might have a 'height' and 'width' property defined in
         * the iframe tag. If that's the case, generate the ratio from these
         * values, otherwise fallback on using scrollHeight/scrollWidth.
         */

        const iframe = element.querySelector("iframe")!

        const iframeSizeRatio = Number(iframe.height) / Number(iframe.width)
        const iframeSizeRatioScroll = iframe.scrollHeight / iframe.scrollWidth

        const sizeRatio = (iframeSizeRatio || iframeSizeRatioScroll) * 100

        if (!sizeRatio) {
            return
        }

        element.style.width = "100%"
        element.style.position = "relative"
        element.style.paddingBottom = `${sizeRatio}%`

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
