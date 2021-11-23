// Remove the row class (Responsive)
let userdata = document.querySelector(".userdata").classList
let windowScreen =  window.screen.width

if (windowScreen < 600) {
    userdata.remove("row");
} else {
    userdata.add("row");
}
