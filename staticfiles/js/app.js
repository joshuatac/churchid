const togglers = document.querySelectorAll(".toggler")
const menubarLinks = document.querySelectorAll(".menubar a")
const menubar = document.querySelector(".menubar")

function ToggleMenu() {
    menubar.classList.toggle("show-menubar")
  
}


togglers.forEach(function(toggler) {
    toggler.onclick = ToggleMenu
})

menubarLinks.forEach(function(menubarLink) {
    menubarLink.onclick = ToggleMenu
})