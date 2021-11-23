// Make table Smaller (Responsive)
let usertable = document.querySelector(".usertable").classList
let windowScreen =  window.screen.width

if (windowScreen < 600) {
    usertable.remove("table")
    usertable.add("table-responsive-sm")
} else {
    usertable.remove("table-responsive-sm")
    usertable.add("table")
}

// check lables
var lables = document.querySelectorAll("table tbody .lable")
for (var i = 0; i < lables.length; i++) {
    var lable = lables[i]
    if (lable.innerText === 'important') {
        lable.style.backgroundColor = 'var(--bs-danger)'
    } else if (lable.innerText === 'too early') {
        lable.style.backgroundColor = 'var(--bs-indigo)'
    } else if (lable.innerText === 'today') {
        lable.style.backgroundColor = 'var(--bs-primary)'
    } else {
        lable.style.backgroundColor = '#000'
    }
}

// Function to close notes
function closeNote(openBtn, note, closeBtn) {
    openBtn.addEventListener("click", () => {
        note.classList.remove("close")
    })
    
    closeBtn.addEventListener("click", () => {
        note.classList.add("close")
    })
}

// open & close add section
var noteAddBtn = document.querySelector("button.add_btn")
var noteAddSection = document.querySelector("section.add_note")
var noteCloseAddBtn = document.querySelector("section.add_note .close_btn")
closeNote(noteAddBtn, noteAddSection, noteCloseAddBtn)

// open & close the note
function viewNote(note) {
    var note_id = document.getElementById(note)
    note_id.classList.toggle("hide_part_of_note")
    note_id.classList.toggle("view_part_of_note")
}

// open & close note again
var noteOpenBtns = document.querySelectorAll("table tbody .note_id")
var noteOpenSection = document.querySelector("section.open_note")
var noteCloseOpenBtn = document.querySelector("section.open_note .close_btn")

