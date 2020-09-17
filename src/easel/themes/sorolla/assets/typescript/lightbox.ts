class Lightbox {
    /*
     * See ./assets/scss/_lightbox.scss for structure.
     * --------------------------------------------------------------------- */

    readonly CLASS_FADE_IN_OUT = "animation--fade-in-out"

    public main = document.querySelector<HTMLDivElement>("#lightbox")!

    public buttonClose = this.main.querySelector<HTMLImageElement>(".lightbox__button--close")!
    public buttonPrev = this.main.querySelector<HTMLImageElement>(".lightbox__button--prev")!
    public buttonNext = this.main.querySelector<HTMLImageElement>(".lightbox__button--next")!

    private containers = this.main.querySelectorAll<HTMLDivElement>(".lightbox__container")
    private items = this.main.querySelectorAll<HTMLImageElement>(".lightbox__item")

    public isVisible: boolean = false
    private currentContainerIndex: number = 0

    private gestureController = new LightboxGestureController(this)
    private uiButtonsController = new LightboxUIButtonsController(this)
    private keyboardController = new LightboxKeyboardController(this)

    setup(): void {
        this.setupEventListeners()
        this.setupLazyLoadImageObserver()
    }

    private setupEventListeners(): void {
        const contentContainers = [...document.querySelectorAll(".content__container")]

        contentContainers.forEach((contentContainer) => {
            contentContainer.addEventListener("click", () => {
                this.show(contentContainers.indexOf(contentContainer))
            })
        })
    }

    private setupLazyLoadImageObserver(): void {
        const lazyLoadImageCallback = (
            entries: IntersectionObserverEntry[],
            observer: IntersectionObserver
        ) => {
            entries.forEach((entry) => {
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
            rootMargin: "0px 0px 0px 0px", // Trigger inside the viewport.
            threshold: 0, // Trigger immediately on viewport enter.
        })

        this.items.forEach((item) => {
            lazyLoadImageObserver.observe(item)
        })
    }

    show(index: number): void {
        this.showContainer(index)
        this.currentContainerIndex = index

        this.isVisible = true
        this.main.classList.add(this.CLASS_FADE_IN_OUT)

        // Prevent body scrolling.
        document.body.style.overflow = "hidden"
    }

    close(): void {
        this.hideContainer(this.currentContainerIndex)

        this.isVisible = false
        this.main.classList.remove(this.CLASS_FADE_IN_OUT)

        // Re-enable body scrolling.
        document.body.style.overflow = "auto"
    }

    next(): void {
        this.hideContainer(this.currentContainerIndex)
        this.showContainer(this.nextContainerIndex)
    }

    prev(): void {
        this.hideContainer(this.currentContainerIndex)
        this.showContainer(this.prevContainerIndex)
    }

    private showContainer(index: number): void {
        this.containers[index].classList.add("show")
    }

    private hideContainer(index: number): void {
        this.containers[index].classList.remove("show")
    }

    private triggerLazyLoadImage(element: HTMLImageElement): void {
        if (!element.dataset.src) {
            return
        }

        element.src = element.dataset.src
    }

    private get nextContainerIndex(): number {
        if (this.currentContainerIndex >= this.containers.length - 1) {
            this.currentContainerIndex = 0
        } else {
            this.currentContainerIndex++
        }

        return this.currentContainerIndex
    }

    private get prevContainerIndex(): number {
        if (this.currentContainerIndex == 0) {
            this.currentContainerIndex = this.containers.length - 1
        } else {
            this.currentContainerIndex--
        }

        return this.currentContainerIndex
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

        if (Math.abs(touchDiff_x) > this.threshold || Math.abs(touchDiff_y) > this.threshold) {
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
    if (!document.querySelector("#lightbox")) {
        return
    }

    new Lightbox().setup()
})
