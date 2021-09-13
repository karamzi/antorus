const switch_buttons = document.querySelectorAll('.switch_buttons_item')
const sliders = document.querySelector('.sliders')
const sections = document.querySelectorAll('.intro_section')
const numberOfSlides_1 = 2
let id = 0


switch_buttons.forEach(item => {
    item.addEventListener('click', switch_slide)
})

sections.forEach(item => {
    item.addEventListener('touchstart', click_slider)
})

function switch_slide() {
    id = +this.getAttribute('data-id')
    sliders.style.transform = 'translateX(' + -100 * id + '%)'

    clearInterval(interval)
    interval = setInterval(time_switch_slider, 10000)
    change_button_color()
}

function time_switch_slider() {
    id === numberOfSlides_1 - 1 ? id = 0 : id += 1
    sliders.style.transform = 'translateX(' + -100 * id + '%)'

    change_button_color()
}

function change_button_color() {
    switch_buttons.forEach(item => {
        const item_id = +item.getAttribute('data-id')
        id === item_id ? item.classList.add('switch_buttons_item_active') : item.classList.remove('switch_buttons_item_active')
    })
}

let start_position
let section

function click_slider(event) {
    start_position = event.touches[0].clientX
    section = this
    window.addEventListener('touchmove', move_slider)
}

function move_slider(event) {
    let difference =  event.touches[0].clientX - start_position

    if (difference < -70) {
        window.removeEventListener('touchmove', move_slider)
        if (id === numberOfSlides_1 - 1) {
            id = 0
        } else {
            id = id + 1
        }
        sliders.style.transform = 'translateX(' + -100 * id + '%)'
    }

    if (difference > 70) {
        window.removeEventListener('touchmove', move_slider)
        if (id === 0) {
            id = numberOfSlides_1 - 1
        } else {
            id = id - 1
        }
        sliders.style.transform = 'translateX(' + -100 * id + '%)'
    }

    clearInterval(interval)
    interval = setInterval(time_switch_slider, 10000)
    change_button_color()
}

let interval = setInterval(time_switch_slider, 10000)
