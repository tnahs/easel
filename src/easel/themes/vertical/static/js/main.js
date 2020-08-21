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