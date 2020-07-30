"use strict";


window.addEventListener("load", function () {

    const menuMobileOpenButton = document.querySelector("#menu-mobile__open-button");
    const menuMobileCloseButton = document.querySelector("#menu-mobile__close-button");

    const menuMobileButtons = document.querySelector(".menu-mobile .menu-mobile__buttons");

    menuMobileOpenButton.addEventListener("click", function () {

        menuMobileButtons.style.opacity = 1;
        menuMobileButtons.style.visibility = "visible";
    });

    menuMobileCloseButton.addEventListener("click", function () {

        menuMobileButtons.style.opacity = 0;
        menuMobileButtons.style.visibility = "hidden";
    });

});
