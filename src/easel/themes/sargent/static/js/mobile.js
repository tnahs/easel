"use strict"

// TODO
class MobileMenu {
    constructor() {}
}

// TODO
class MobileMenuKeyboardController {
    constructor() {}
}

// TODO
class MobileMenuUIButtonsController {
    constructor() {}
}

window.addEventListener("load", () => {
    const CLASS_ANIMATE = "animate__fade-in-out"

    function animateFadeIn(content) {
        content.classList.add(CLASS_ANIMATE)
    }

    function animateFadeOut(content) {
        content.classList.remove(CLASS_ANIMATE)
    }

    const menuMobileButtonOpen = document.querySelector(
        "#menu-mobile-button-open"
    )
    const menuMobileButtonClose = document.querySelector(
        "#menu-mobile-button-close"
    )

    const menuMobile = document.querySelector("#menu-mobile")
    const menuMobileButtons = menuMobile.querySelector(".menu-items")
    const menuMobileFooter = menuMobile.querySelector("#menu-footer")

    menuMobileButtonOpen.addEventListener("click", function () {
        this.style.display = "none"
        menuMobileButtonClose.style.display = "block"

        animateFadeIn(menuMobile)
        animateFadeIn(menuMobileButtons)
        animateFadeIn(menuMobileFooter)

        // Prevent body scrolling.
        document.body.style.overflow = "hidden"
    })

    menuMobileButtonClose.addEventListener("click", function () {
        this.style.display = "none"
        menuMobileButtonOpen.style.display = "block"

        animateFadeOut(menuMobile)
        animateFadeOut(menuMobileButtons)
        animateFadeOut(menuMobileFooter)

        document.body.style.overflow = "auto"
    })

    document.addEventListener("keydown", (event) => {
        if (!menuMobile.classList.contains("animate__fade-in-out")) {
            return
        }

        if (event.code == "Escape") {
            animateFadeOut(menuMobile)
            animateFadeOut(menuMobileButtons)
            animateFadeOut(menuMobileFooter)
        }
    })
})
