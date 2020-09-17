"use strict"

class Lightbox {
    /*
     * See ./assets/scss/_lightbox.scss for structure.
     * --------------------------------------------------------------------- */

    private CLASS_FADE_IN_OUT = "animation--fade-in-out"

    main = document.querySelector<HTMLElement>("#lightbox")

    buttonClose = this.main.querySelector<HTMLElement>(
        ".lightbox__button--close"
    )
    buttonPrev = this.main.querySelector<HTMLElement>(".lightbox__button--prev")
    buttonNext = this.main.querySelector<HTMLElement>(".lightbox__button--next")

    private containers = this.main.querySelectorAll<HTMLElement>(
        ".lightbox__container"
    )

    private items = this.main.querySelectorAll<HTMLElement>(".lightbox__item")
    private items__toLazyLoad = [...this.items].filter((item) =>
        item.hasAttribute("data-src")
    )

    isVisible: boolean

    private currentIndex: number | null

    private gestureController = new LightboxGestureController(this)
    private uiButtonsController = new LightboxUIButtonsController(this)
    private keyboardController = new LightboxKeyboardController(this)

    constructor() {
        this.isVisible = false
        this.currentIndex = null
    }

    setup(): void {
        this.setupEventListeners()
        this.setupLazyLoadObserver()
    }

    private setupEventListeners(): void {
        const contentContainers = [
            ...document.querySelectorAll(".content__container"),
        ]

        contentContainers.forEach((contentContainer) => {
            contentContainer.addEventListener("click", () => {
                this.show(contentContainers.indexOf(contentContainer))
            })
        })
    }

    private setupLazyLoadObserver(): void {
        const lazyLoadCallback = (
            entries: IntersectionObserverEntry[],
            observer: IntersectionObserver
        ) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return
                }

                this.triggerLazyLoad(<HTMLImageElement>entry.target)

                observer.unobserve(entry.target)
            })
        }

        const lazyLoadObserver = new IntersectionObserver(lazyLoadCallback)

        this.items__toLazyLoad.forEach((lightboxItem) => {
            lazyLoadObserver.observe(lightboxItem)
        })
    }

    show(index: number): void {
        this.showContainer(index)
        this.currentIndex = index

        this.isVisible = true
        this.main.classList.add(this.CLASS_FADE_IN_OUT)

        // Prevent body scrolling.
        document.body.style.overflow = "hidden"
    }

    close(): void {
        this.hideContainer(this.currentIndex)
        this.currentIndex = null

        this.isVisible = false
        this.main.classList.remove(this.CLASS_FADE_IN_OUT)

        // Re-enable body scrolling.
        document.body.style.overflow = "auto"
    }

    next(): void {
        this.hideContainer(this.currentIndex)
        this.showContainer(this.nextIndex)
    }

    prev(): void {
        this.hideContainer(this.currentIndex)
        this.showContainer(this.prevIndex)
    }

    private showContainer(index: number): void {
        this.containers[index].classList.add("show")
    }

    private hideContainer(index: number): void {
        this.containers[index].classList.remove("show")
    }

    private triggerLazyLoad(element: HTMLImageElement): void {
        element.src = element.dataset.src
    }

    private get nextIndex(): number {
        if (this.currentIndex >= this.containers.length - 1) {
            this.currentIndex = 0
        } else {
            this.currentIndex++
        }

        return this.currentIndex
    }

    private get prevIndex(): number {
        if (this.currentIndex == 0) {
            this.currentIndex = this.containers.length - 1
        } else {
            this.currentIndex--
        }

        return this.currentIndex
    }
}

abstract class LightboxController {
    protected lightbox: Lightbox

    constructor(lightbox: Lightbox) {
        this.lightbox = lightbox
        this.setup()
    }

    protected abstract setup(): void
}

class LightboxUIButtonsController extends LightboxController {
    protected setup(): void {
        this.lightbox.buttonClose.addEventListener("click", () => {
            this.lightbox.close()
        })

        this.lightbox.buttonPrev.addEventListener("click", () => {
            this.lightbox.prev()
        })

        this.lightbox.buttonNext.addEventListener("click", () => {
            this.lightbox.next()
        })
    }
}

class LightboxKeyboardController extends LightboxController {
    protected setup(): void {
        document.addEventListener("keydown", (event) => {
            if (!this.lightbox.isVisible) {
                return
            }

            if (event.code == "Escape") {
                this.lightbox.close()
            } else if (event.code == "ArrowLeft") {
                this.lightbox.prev()
            } else if (event.code == "ArrowRight") {
                this.lightbox.next()
            }
        })
    }
}

class LightboxGestureController extends LightboxController {
    // TODO:HIGH Implement 'hammer.js' instead.

    private deviceWidth = window.innerWidth || document.body.clientWidth
    private threshold = Math.max(1, Math.floor(0.01 * this.deviceWidth))
    private limit = Math.tan(((45 * 1.5) / 180) * Math.PI)

    private touchStart_x: number = 0
    private touchStart_y: number = 0
    private touchEnd_x: number = 0
    private touchEnd_y: number = 0

    protected setup(): void {
        this.lightbox.main.addEventListener(
            "touchstart",
            (event: TouchEvent) => {
                this.touchStart_x = event.changedTouches[0].screenX
                this.touchStart_y = event.changedTouches[0].screenY
            },
            false
        )

        this.lightbox.main.addEventListener(
            "touchend",
            (event: TouchEvent) => {
                this.touchEnd_x = event.changedTouches[0].screenX
                this.touchEnd_y = event.changedTouches[0].screenY

                this._handleGesture()
            },
            false
        )
    }

    _handleGesture(): void {
        const touchDiff_x = this.touchEnd_x - this.touchStart_x
        const touchDiff_y = this.touchEnd_y - this.touchStart_y
        const touchDiffRatio_xy = Math.abs(touchDiff_x / touchDiff_y)
        const touchDiffRatio_yx = Math.abs(touchDiff_y / touchDiff_x)

        if (
            Math.abs(touchDiff_x) > this.threshold ||
            Math.abs(touchDiff_y) > this.threshold
        ) {
            if (touchDiffRatio_yx <= this.limit) {
                if (touchDiff_x < 0) {
                    // Gesture: Swipe Left
                    this.lightbox.prev()
                } else {
                    // Gesture: Swipe Right
                    this.lightbox.next()
                }
            }

            if (touchDiffRatio_xy <= this.limit) {
                if (touchDiff_y < 0) {
                    // Gesture: Swipe Up
                    this.lightbox.close()
                } else {
                    // Gesture: Swipe Down
                    this.lightbox.close()
                }
            }
        }
    }
}

window.addEventListener("load", () => {
    if (document.querySelector("#lightbox") === null) {
        return
    }

    new Lightbox().setup()
})
