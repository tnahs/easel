"use strict"

class MenuMobile {
    /*
     * See static/css/menu-mobile.css for structure.
     * --------------------------------------------------------------------- */

    constructor() {
        this.CLASS_FADE_IN_OUT = "animation__fade-in-out"

        this.main = document.querySelector("#menu-mobile")
        this.menuItems = document.querySelector(".menu-mobile__menu-items")
        this.footer = document.querySelector(".menu-mobile__footer")

        this.buttons = document.querySelector("#menu-mobile-buttons")
        this.buttonOpen = document.querySelector(".menu-mobile-button--open")
        this.buttonClose = document.querySelector(".menu-mobile-button--close")

        /// TODO:LOW The above attributes are class-attributes. They are placed
        // inside the constructor for Safari support. Re-work when converting
        // to TypeScript.

        this.isVisible = false

        this.menuElements__toFadeIn = [this.main, this.menuItems, this.footer]

        this._uiButtonsController = new MenuMobileUIButtonsController(this)
        this._keyboardController = new MenuMobileKeyboardController(this)
    }

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
})
