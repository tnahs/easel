"use strict"

// TODO
class ContentPlaceholder {
    constructor() {}
}

window.addEventListener("load", () => {
    const DEFAULT_PLACEHOLDER_COLOR = "rgba(0, 0, 0, .05)"
    const PLACEHOLDER_COLOR_ALPHA = "0.75"

    const contentItems = document.querySelectorAll(
        "#page-contents .content-container .content-item"
    )

    contentItems.forEach((contentItem) => {
        const contentImage = contentItem.querySelector(".image")

        if (!contentImage) {
            return
        }

        let placeholderColor

        try {
            placeholderColor = JSON.parse(contentImage.dataset.placeholderColor)
        } catch {
            placeholderColor = DEFAULT_PLACEHOLDER_COLOR
        }

        if (!placeholderColor.length) {
            placeholderColor = DEFAULT_PLACEHOLDER_COLOR
        } else {
            placeholderColor = `
                rgba(
                    ${placeholderColor[0]},
                    ${placeholderColor[1]},
                    ${placeholderColor[2]},
                    ${PLACEHOLDER_COLOR_ALPHA}
                    )
                `
        }

        contentItem.style.backgroundColor = placeholderColor
    })
})

window.addEventListener("load", () => {
    function animateFadeIn(element) {
        element.classList.add("animate__fade-in")
    }

    function lazyLoadElement(element) {
        if (element.dataset.src === undefined) {
            return
        }

        element.src = element.dataset.src
    }

    const lazyLoadObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    if (entry.intersectionRatio > 0) {
                        lazyLoadElement(entry.target)
                        observer.unobserve(entry.target)
                    }
                }
            })
        },
        { rootMargin: "0px 0px -50% 0px" }
    )

    const fadeInObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    if (entry.intersectionRatio > 0) {
                        animateFadeIn(entry.target)
                        observer.unobserve(entry.target)
                    }
                }
            })
        },
        { rootMargin: "0px 0px -20% 0px" }
    )

    const contentItems = document.querySelectorAll(
        "#page-contents .content-container .content-item > *, .content-caption"
    )

    contentItems.forEach((contentImage) => {
        fadeInObserver.observe(contentImage)
        lazyLoadObserver.observe(contentImage)
    })
})

window.addEventListener("load", () => {
    const embeddedElements = document.querySelectorAll(".embedded iframe")

    for (const element of embeddedElements) {
        /**
         * Some elements might have a 'height' and 'width' property defined in
         * the iframe tag. If that's the case, generate the ratio from these
         * values, otherwise fallback on using scrollHeight/scrollWidth.
         */

        const _sizeRatio = element.height / element.width
        const _sizeRatioScroll = element.scrollHeight / element.scrollWidth

        const sizeRatio = (_sizeRatio || _sizeRatioScroll || 0) * 100

        if (!sizeRatio) {
            continue
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
})
