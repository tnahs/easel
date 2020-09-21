type Color = {
    R: number
    G: number
    B: number
}

/*
 * See ./src/scss/layouts/_contents.scss for structure.
 * ------------------------------------------------------------------------- */

class AllContentItems {
    readonly FADE_IN_CLASS = "animation--fade-in"
    readonly FADE_DELAY = 500

    private containers = document.querySelectorAll<HTMLDivElement>(".content__container")!

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
                    this.triggerFadeIn(<HTMLDivElement>entry.target)
                }, this.FADE_DELAY)

                observer.unobserve(entry.target)
            })
        }

        const fadeInObserver = new IntersectionObserver(fadeInCallback, {
            root: null, // Observe entire viewport.
            rootMargin: "0px 0px 0px 0px", // Trigger inside the viewport.
            threshold: 0, // Trigger immediately on viewport enter.
        })

        this.containers.forEach((element) => {
            fadeInObserver.observe(element)
        })
    }

    private triggerFadeIn(element: HTMLDivElement): void {
        element.classList.add(this.FADE_IN_CLASS)
    }
}

class ImageContentItems {
    private items = document.querySelectorAll<HTMLDivElement>(".content--image")!

    setup(): void {
        this.setupLazyLoadImageObserver()
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

                this.triggerLazyLoadImage(<HTMLDivElement>entry.target)

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

    // TODO:HIGH Fix image flickering on load.
    private triggerLazyLoadImage(element: HTMLDivElement): void {
        const image = element.querySelector("img")!

        if (!image.dataset.src) {
            return
        }

        image.src = image.dataset.src
    }
}

class EmbeddedContentItems {
    private items = document.querySelectorAll<HTMLDivElement>(".content--embedded")

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

        const iframeSizeRatio = +iframe.height / +iframe.width
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
