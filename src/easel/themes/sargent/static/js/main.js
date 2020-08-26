"use strict"


window.addEventListener("load", () => {

    const menuMobileOpenButton = document.querySelector("#menu-mobile__open-button")
    const menuMobileCloseButton = document.querySelector("#menu-mobile__close-button")

    const menuMobileButtons = document.querySelector(".menu-mobile .menu-mobile__buttons")

    menuMobileOpenButton.addEventListener("click", () => {

        menuMobileButtons.style.opacity = 1
        menuMobileButtons.style.visibility = "visible"
    })

    menuMobileCloseButton.addEventListener("click", () => {

        menuMobileButtons.style.opacity = 0
        menuMobileButtons.style.visibility = "hidden"
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


//

window.addEventListener("load", () => {

    //
    const DEFAULT_PLACEHOLDER_COLOR = "rgba(0, 0, 0, .05)"
    const contentItems = document.querySelectorAll(".content-item")

    contentItems.forEach(contentItem => {

        const contentImage = contentItem.querySelector(".image")

        if (!contentImage) {
            return
        }

        let placeholderColor = JSON.parse(contentImage.dataset.placeholderColor)

        if (!placeholderColor.length) {

            placeholderColor = DEFAULT_PLACEHOLDER_COLOR

        } else {

            placeholderColor = `
                rgba(
                    ${placeholderColor[0]},
                    ${placeholderColor[1]},
                    ${placeholderColor[2]},
                    0.5
                )
            `
        }

        contentItem.style.backgroundColor = placeholderColor
    })

    //

    function animateFadeIn(content) {
        content.classList.add("animate__fade-in")
    }

    function lazyLoadContent(content) {
        content.src = content.dataset.src
    }

    //
    const lazyLoadObserver = new IntersectionObserver((entries, observer) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                if (entry.intersectionRatio > 0) {

                    lazyLoadContent(entry.target)
                    observer.unobserve(entry.target)
                }
            }
        })
    }, {rootMargin: "0px 0px -50% 0px"})


    //
    const stateSetObserver = new IntersectionObserver((entries, observer) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                if (entry.intersectionRatio > 0) {

                    animateFadeIn(entry.target)
                    observer.unobserve(entry.target)
                }
            }
        })
    }, {rootMargin: "0px 0px -20% 0px"})

    const contentItemImages = document.querySelectorAll(".content-item .image")

    contentItemImages.forEach(contentImage => {
        stateSetObserver.observe(contentImage)
        lazyLoadObserver.observe(contentImage)
    })
})