"use strict"

class Lightbox {
    /*
     * See static/css/lightbox.css for structure.
     * --------------------------------------------------------------------- */

    constructor() {
        this.CLASS_FADE_IN_OUT = "animation__fade-in-out"

        this.main = document.querySelector("#lightbox")

        this.buttonClose = document.querySelector(".lightbox__button--close")
        this.buttonPrev = document.querySelector(".lightbox__button--prev")
        this.buttonNext = document.querySelector(".lightbox__button--next")

        this.lightboxContainers = document.querySelectorAll(
            ".lightbox__container"
        )
        this.lightboxItems = document.querySelectorAll(".lightbox__item")

        // TODO:LOW The above attributes are class-attributes. They are placed
        // inside the constructor for Safari support. Re-work when converting
        // to TypeScript.

        this.isVisible = false
        this.currentIndex = null

        this.lightboxItems__toLazyLoad = [
            ...this.lightboxItems,
        ].filter((item) => item.hasAttribute("data-src"))

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

        this.lightboxItems__toLazyLoad.forEach((lightboxItem) => {
            lazyLoadObserver.observe(lightboxItem)
        })
    }

    show(index) {
        this._showContainer(index)
        this.currentIndex = index
        this._show()
    }

    close() {
        this._hideContainer(this.currentIndex)
        this.currentIndex = null
        this._close()
    }

    next() {
        this._hideContainer(this.currentIndex)
        this._showContainer(this._nextIndex)
    }

    prev() {
        this._hideContainer(this.currentIndex)
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
        this.lightboxContainers[index].classList.add("show")
    }

    _hideContainer(index) {
        this.lightboxContainers[index].classList.remove("show")
    }

    _triggerLazyLoad(element) {
        element.src = element.dataset.src
    }

    get _nextIndex() {
        if (this.currentIndex >= this.lightboxContainers.length - 1) {
            this.currentIndex = 0
        } else {
            this.currentIndex++
        }

        return this.currentIndex
    }

    get _prevIndex() {
        if (this.currentIndex == 0) {
            this.currentIndex = this.lightboxContainers.length - 1
        } else {
            this.currentIndex--
        }

        return this.currentIndex
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
    // TODO:HIGH Implement 'hammer.js' instead.
    constructor(lightbox) {
        this._lightbox = lightbox

        this.deviceWidth = window.innerWidth || document.body.clientWidth
        this.threshold = Math.max(1, Math.floor(0.01 * this.deviceWidth))
        this.limit = Math.tan(((45 * 1.5) / 180) * Math.PI)

        this.touchStart_x = 0
        this.touchStart_y = 0
        this.touchEnd_x = 0
        this.touchEnd_y = 0

        this.setup()
    }

    setup() {
        this._lightbox.main.addEventListener(
            "touchstart",
            (event) => {
                this.touchStart_x = event.changedTouches[0].screenX
                this.touchStart_y = event.changedTouches[0].screenY
            },
            false
        )

        this._lightbox.main.addEventListener(
            "touchend",
            (event) => {
                this.touchEnd_x = event.changedTouches[0].screenX
                this.touchEnd_y = event.changedTouches[0].screenY

                this._handleGesture()
            },
            false
        )
    }

    _handleGesture() {
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
                    this._lightbox.prev()
                } else {
                    // Gesture: Swipe Right
                    this._lightbox.next()
                }
            }

            if (touchDiffRatio_xy <= this.limit) {
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
