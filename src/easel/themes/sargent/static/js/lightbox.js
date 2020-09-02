"use strict"

class Lightbox {
    /**
     * <div id=lightbox">
     *     <div id="lightbox-contents">
     *         <div class="content-container">
     *             <div class="content-item">
     *                 <content></content>
     *             </div>
     *             <div class="content-caption">
     *                 <div class="caption-title"></div>
     *                 <div class="caption-description"></div>
     *             </div>
     *         </div>
     *     </div>
     * </div>
     */
    constructor() {
        this.CLASS_FADE_IN_OUT = "animate__fade-in-out"

        this.isVisible = false

        this._currentIndex = null

        this._main = document.querySelector("#lightbox")

        this._contentContainers = this._main.querySelectorAll(
            "#lightbox-contents .content-container"
        )

        this._galleryContentContainers = document.querySelectorAll(
            "#page-contents .content-container"
        )

        this._gestureController = new LightboxGestureController(this)
        this._uiButtonsController = new LightboxUIButtonsController(this)
        this._keyboardController = new LightboxKeyboardController(this)

        this._lazyLoadObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        if (entry.intersectionRatio > 0) {
                            this._lazyLoadContents(entry.target)
                            observer.unobserve(entry.target)
                        }
                    }
                })
            }
        )
    }

    setup() {
        this._galleryContentContainers.forEach((contentContainer) => {
            contentContainer.addEventListener("click", () => {
                let index = Array.prototype.indexOf.call(
                    this._galleryContentContainers,
                    contentContainer
                )
                this.show(index)
            })
        })

        this._contentContainers.forEach((contentContainer) => {
            this._lazyLoadObserver.observe(contentContainer)
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
        this._main.classList.add(this.CLASS_FADE_IN_OUT)
        document.body.style.overflow = "hidden"
    }

    _close() {
        this.isVisible = false
        this._main.classList.remove(this.CLASS_FADE_IN_OUT)
        document.body.style.overflow = "auto"
    }

    _showContainer(index) {
        this._contentContainers[index].style.display = "block"
    }

    _hideContainer(index) {
        this._contentContainers[index].style.display = "none"
    }

    _lazyLoadContents(container) {
        let item = container.querySelector(".image")

        if (item.dataset.src === undefined) {
            return
        }
        item.src = item.dataset.src
    }
    get _nextIndex() {
        if (this._currentIndex >= this._contentContainers.length - 1) {
            this._currentIndex = 0
        } else {
            this._currentIndex++
        }

        return this._currentIndex
    }

    get _prevIndex() {
        if (this._currentIndex == 0) {
            this._currentIndex = this._contentContainers.length - 1
        } else {
            this._currentIndex--
        }

        return this._currentIndex
    }
}

class LightboxUIButtonsController {
    constructor(lightbox) {
        this._lightbox = lightbox

        this._buttonClose = this._lightbox._main.querySelector(
            "#lightbox-button-close"
        )
        this._buttonPrev = this._lightbox._main.querySelector(
            "#lightbox-button-prev"
        )
        this._buttonNext = this._lightbox._main.querySelector(
            "#lightbox-button-next"
        )

        this.setup()
    }

    setup() {
        this._buttonClose.addEventListener("click", () => {
            this._lightbox.close()
        })

        this._buttonPrev.addEventListener("click", () => {
            this._lightbox.prev()
        })

        this._buttonNext.addEventListener("click", () => {
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
        this._lightbox._main.addEventListener(
            "touchstart",
            (event) => {
                this._touchStart_x = event.changedTouches[0].screenX
                this._touchStart_y = event.changedTouches[0].screenY
            },
            false
        )

        this._lightbox._main.addEventListener(
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
        let touchDiff_x = this._touchEnd_x - this._touchStart_x
        let touchDiff_y = this._touchEnd_y - this._touchStart_y

        let touchDiffRatio_xy = Math.abs(touchDiff_x / touchDiff_y)
        let touchDiffRatio_yx = Math.abs(touchDiff_y / touchDiff_x)

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
