class MenuMobile {
    /*
     * See ./src/scss/layouts/_menu-mobile.scss for structure.
     * --------------------------------------------------------------------- */

    readonly FADE_IN_OUT_CLASS = "animation--fade-in-out"
    readonly FADE_IN_OUT_DELAY: number = 25

    toggles = document.querySelector<HTMLElement>("#menu-mobile-toggles")!
    toggleOpen = this.toggles.querySelector<HTMLElement>(".menu-mobile-toggle--open")!
    toggleClose = this.toggles.querySelector<HTMLElement>(".menu-mobile-toggle--close")!

    private main = document.querySelector<HTMLElement>("#menu-mobile")!
    private menuItems = this.main.querySelectorAll<HTMLElement>(".menu-item")!
    private footer = this.main.querySelector<HTMLElement>(".menu-mobile__footer")!

    private elements__toFadeIn = [this.main, ...this.menuItems, this.footer]
    private elements__toFadeOut = [...this.elements__toFadeIn].reverse()

    private keyboardController = new MenuMobileKeyboardController(this)
    private uiTogglesController = new MenuMobileUITogglesController(this)

    isVisible: boolean = false

    setup(): void {
        this.close()
    }

    open(): void {
        this.elements__toFadeIn.forEach((element, count) => {
            setTimeout(() => {
                element.classList.add(this.FADE_IN_OUT_CLASS)
            }, count * this.FADE_IN_OUT_DELAY)
        })

        this.isVisible = true
        this.toggleOpen.style.display = "none"
        this.toggleClose.style.display = "block"

        // Prevent body scrolling.
        document.body.style.overflow = "hidden"
    }

    close(): void {
        this.elements__toFadeOut.forEach((element, count) => {
            setTimeout(() => {
                element.classList.remove(this.FADE_IN_OUT_CLASS)
            }, count * this.FADE_IN_OUT_DELAY)
        })

        this.isVisible = false
        this.toggleOpen.style.display = "block"
        this.toggleClose.style.display = "none"

        // Re-enable body scrolling.
        document.body.style.overflow = "auto"
    }
}

abstract class MenuMobileController {
    protected menuMobile: MenuMobile

    constructor(menuMobile: MenuMobile) {
        this.menuMobile = menuMobile
        this.setup()
    }

    protected abstract setup(): void
}

class MenuMobileUITogglesController extends MenuMobileController {
    protected setup(): void {
        this.menuMobile.toggleOpen.addEventListener("click", () => {
            this.menuMobile.open()
        })
        this.menuMobile.toggleClose.addEventListener("click", () => {
            this.menuMobile.close()
        })
    }
}

class MenuMobileKeyboardController extends MenuMobileController {
    protected setup(): void {
        document.addEventListener("keydown", (event) => {
            if (!this.menuMobile.isVisible) {
                return
            }

            if (event.code == "Escape") {
                this.menuMobile.close()
            }
        })
    }
}

window.addEventListener("load", () => {
    new MenuMobile().setup()
})
