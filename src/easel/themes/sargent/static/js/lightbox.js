"use strict"

class Lightbox {
    /** Structure of #lightbox

        #lightbox
            .lightbox__container
                .lightbox-item__image
                .lightbox__caption
                    .caption
                        .caption__title
                        .caption__description
    ------------------------------------------------------------------------ */
    constructor() {
        this.CLASS_FADE_IN_OUT = "animation__fade-in-out"

        this.isVisible = false

        this._currentIndex = null

        this.main = document.querySelector("#lightbox")

        this.buttonClose = document.querySelector("#lightbox__button-close")
        this.buttonPrev = document.querySelector("#lightbox__button-prev")
        this.buttonNext = document.querySelector("#lightbox__button-next")

        this._lightboxContainers = document.querySelectorAll(
            ".lightbox__container"
        )

        this._lightboxItems = [
            ...document.querySelectorAll("[class^='lightbox-item__']"),
        ]

        this._lightboxItems__toLazyLoad = this._lightboxItems.filter((item) =>
            item.hasAttribute("data-src")
        )

        this._gestureController = new LightboxGestureController(this)
        this._uiButtonsController = new LightboxUIButtonsController(this)
        this._keyboardController = new LightboxKeyboardController(this)
    }

    setup() {
        this._setupEventListeners()
        this._setupLazyLoadObserver()
    }

    _setupEventListeners() {
        const contentContainers = document.querySelectorAll(
            ".content__container"
        )

        contentContainers.forEach((contentContainer) => {
            contentContainer.addEventListener("click", () => {
                let index = Array.prototype.indexOf.call(
                    contentContainers,
                    contentContainer
                )
                this.show(index)
            })
        })
    }

    _setupLazyLoadObserver() {
        const lazyLoadCallback = (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return
                }

                this._triggerLazyLoad(entry.target)

                observer.unobserve(entry.target)
            })
        }

        const lazyLoadObserver = new IntersectionObserver(lazyLoadCallback)

        this._lightboxItems__toLazyLoad.forEach((lightboxItem) => {
            lazyLoadObserver.observe(lightboxItem)
        })
    }

    show(index) {
        this._showContainer(index)
        this._currentIndex = index
        this._show()
    }

    close() {
        this._hideContainer(this._currentIndex)
        this._currentIndex = null
        this._close()
    }

    next() {
        this._hideContainer(this._currentIndex)
        this._showContainer(this._nextIndex)
    }

    prev() {
        this._hideContainer(this._currentIndex)
        this._showContainer(this._prevIndex)
    }

    _show() {
        this.isVisible = true
        this.main.classList.add(this.CLASS_FADE_IN_OUT)

        // Prevent body scrolling.
        document.body.style.overflow = "hidden"
    }

    _close() {
        this.isVisible = false
        this.main.classList.remove(this.CLASS_FADE_IN_OUT)

        // Re-enable body scrolling.
        document.body.style.overflow = "auto"
    }

    _showContainer(index) {
        this._lightboxContainers[index].style.display = "block"
    }

    _hideContainer(index) {
        this._lightboxContainers[index].style.display = "none"
    }

    _triggerLazyLoad(element) {
        element.src = element.dataset.src
    }

    get _nextIndex() {
        if (this._currentIndex >= this._lightboxContainers.length - 1) {
            this._currentIndex = 0
        } else {
            this._currentIndex++
        }

        return this._currentIndex
    }

    get _prevIndex() {
        if (this._currentIndex == 0) {
            this._currentIndex = this._lightboxContainers.length - 1
        } else {
            this._currentIndex--
        }

        return this._currentIndex
    }
}

class LightboxUIButtonsController {
    constructor(lightbox) {
        this._lightbox = lightbox

        this.setup()
    }

    setup() {
        this._lightbox.buttonClose.addEventListener("click", () => {
            this._lightbox.close()
        })

        this._lightbox.buttonPrev.addEventListener("click", () => {
            this._lightbox.prev()
        })

        this._lightbox.buttonNext.addEventListener("click", () => {
            this._lightbox.next()
        })
    }
}

class LightboxKeyboardController {
    constructor(lightbox) {
        this._lightbox = lightbox

        this.setup()
    }

    setup() {
        document.addEventListener("keydown", (event) => {
            if (!this._lightbox.isVisible) {
                return
            }

            if (event.code == "Escape") {
                this._lightbox.close()
            } else if (event.code == "ArrowLeft") {
                this._lightbox.prev()
            } else if (event.code == "ArrowRight") {
                this._lightbox.next()
            }
        })
    }
}

class LightboxGestureController {
    // TODO: Ignore pinch/zoom.
    constructor(lightbox) {
        this._lightbox = lightbox

        this._deviceWidth = window.innerWidth || document.body.clientWidth
        this._threshold = Math.max(1, Math.floor(0.01 * this._deviceWidth))
        this._limit = Math.tan(((45 * 1.5) / 180) * Math.PI)

        this._touchStart_x = 0
        this._touchStart_y = 0
        this._touchEnd_x = 0
        this._touchEnd_y = 0

        this.setup()
    }

    setup() {
        this._lightbox.main.addEventListener(
            "touchstart",
            (event) => {
                this._touchStart_x = event.changedTouches[0].screenX
                this._touchStart_y = event.changedTouches[0].screenY
            },
            false
        )

        this._lightbox.main.addEventListener(
            "touchend",
            (event) => {
                this._touchEnd_x = event.changedTouches[0].screenX
                this._touchEnd_y = event.changedTouches[0].screenY

                this._handleGesture()
            },
            false
        )
    }

    _handleGesture() {
        const touchDiff_x = this._touchEnd_x - this._touchStart_x
        const touchDiff_y = this._touchEnd_y - this._touchStart_y
        const touchDiffRatio_xy = Math.abs(touchDiff_x / touchDiff_y)
        const touchDiffRatio_yx = Math.abs(touchDiff_y / touchDiff_x)

        if (
            Math.abs(touchDiff_x) > this._threshold ||
            Math.abs(touchDiff_y) > this._threshold
        ) {
            if (touchDiffRatio_yx <= this._limit) {
                if (touchDiff_x < 0) {
                    // Gesture: Swipe Left
                    this._lightbox.prev()
                } else {
                    // Gesture: Swipe Right
                    this._lightbox.next()
                }
            }

            if (touchDiffRatio_xy <= this._limit) {
                if (touchDiff_y < 0) {
                    // Gesture: Swipe Up
                    this._lightbox.close()
                } else {
                    // Gesture: Swipe Down
                    this._lightbox.close()
                }
            }
        }
    }
}

window.addEventListener("load", () => {
    const lightbox = new Lightbox()

    lightbox.setup()
})
