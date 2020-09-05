"use strict"

class MenuMobile {
    /** Structure of #menu-mobile-buttons & #menu-mobile

        #menu-mobile-buttons
            #menu-mobile-buttons__open
            #menu-mobile-buttons__close

        #menu-mobile
            #menu-mobile__menu-items
                .menu-item__link-page
                .menu-item__link-url
                    .menu-item__spacer
                    .menu-item__spacer--small
                    .menu-item__spacer--medium
                    .menu-item__spacer--large
            #menu-mobile__footer
    ------------------------------------------------------------------------ */

    CLASS_FADE_IN_OUT = "animation__fade-in-out"

    main = document.querySelector("#menu-mobile")

    buttons = document.querySelector("#menu-mobile-buttons")
    buttonOpen = document.querySelector("#menu-mobile-buttons__open")
    buttonClose = document.querySelector("#menu-mobile-buttons__close")

    menuItems = document.querySelector("#menu-mobile__menu-items")
    footer = document.querySelector("#menu-mobile__footer")

    constructor() {
        this.isVisible = false

        this.menuElements__toFadeIn = [this.main, this.menuItems, this.footer]

        this._uiButtonsController = new MenuMobileUIButtonsController(this)
        this._keyboardController = new MenuMobileKeyboardController(this)
    }

    setup() {}

    open() {
        this.menuElements__toFadeIn.forEach((menuElement) => {
            menuElement.classList.add(this.CLASS_FADE_IN_OUT)
        })

        this.isVisible = true
        this.buttonOpen.style.display = "none"
        this.buttonClose.style.display = "block"

        // Prevent body scrolling.
        document.body.style.overflow = "hidden"
    }

    close() {
        this.menuElements__toFadeIn.forEach((menuElement) => {
            menuElement.classList.remove(this.CLASS_FADE_IN_OUT)
        })

        this.isVisible = false
        this.buttonOpen.style.display = "block"
        this.buttonClose.style.display = "none"

        // Re-enable body scrolling.
        document.body.style.overflow = "auto"
    }
}

class MenuMobileUIButtonsController {
    constructor(menuMobile) {
        this._menuMobile = menuMobile

        this.setup()
    }

    setup() {
        this._menuMobile.buttonOpen.addEventListener("click", () => {
            this._menuMobile.open()
        })
        this._menuMobile.buttonClose.addEventListener("click", () => {
            this._menuMobile.close()
        })
    }
}

class MenuMobileKeyboardController {
    constructor(menuMobile) {
        this._menuMobile = menuMobile

        this.setup()
    }

    setup() {
        document.addEventListener("keydown", (event) => {
            if (!this._menuMobile.isVisible) {
                return
            }

            if (event.code == "Escape") {
                this._menuMobile.close()
            }
        })
    }
}

window.addEventListener("load", () => {
    const menuMobile = new MenuMobile()

    menuMobile.setup()
})
