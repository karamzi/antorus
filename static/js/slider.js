const productBlock = document.querySelector('.suggestions_products')
const products = document.querySelectorAll('.suggestions_product_item')
let sliderButtons = document.querySelectorAll('.suggestions_switch_button')
let hiddenProductCount = products.length - 4
let position = 0
let step = 25
let speed = 1

window.addEventListener(`resize`, main)

function main() {
    adjustSlider()
    createSwitchButtons(hiddenProductCount)
    sliderButtons = document.querySelectorAll('.suggestions_switch_button')
    sliderButtons.forEach(slider)
}

function adjustSlider() {
    position = 0
    productBlock.style.transform = 'translateX(0%)'
    if (window.innerWidth > 900) {
        products.forEach(item => {
            item.style.minWidth = '25%'
        })
    }

    if (window.innerWidth <= 900) {
        products.forEach(item => {
            item.style.minWidth = '33.333%'
        })
        step = 33.333
        speed = 1
        hiddenProductCount = products.length - 3
    }

    if (window.innerWidth <= 700) {
        products.forEach(item => {
            item.style.minWidth = '50%'
        })
        step = 50
        speed = 2.5
        hiddenProductCount = products.length - 2
    }

    if (window.innerWidth <= 500) {
        products.forEach(item => {
            item.style.minWidth = '100%'
        })
        step = 100
        speed = 5
        hiddenProductCount = products.length - 1
    }
}

function slider(item) {
    item.addEventListener('click', function () {
        const activeId = +document.querySelector('.suggestions_switch_button_active').getAttribute('data-id')
        const currentId = +this.getAttribute('data-id')
        if (currentId > activeId) {
            const moveSlider = setInterval(() => {
                position -= speed
                productBlock.style.transform = 'translateX(' + position + '%)'
                if (position <= currentId * -step) {
                    return clearInterval(moveSlider)
                }
            }, 10)
        } else if (currentId < activeId) {
            const moveSlider = setInterval(() => {
                position += speed
                productBlock.style.transform = 'translateX(' + position + '%)'
                if (position >= currentId * -step) {
                    return clearInterval(moveSlider)
                }
            }, 10)
        }
        sliderButtons.forEach(removeActiveClass)
        this.classList.add('suggestions_switch_button_active')
    })
}

function removeActiveClass(item) {
    item.classList.remove('suggestions_switch_button_active')
}

function createSwitchButtons(buttons) {
    let html = '<button data-id="0" class="suggestions_switch_button suggestions_switch_button_active"></button>'
    for (let i = 1; i <= buttons; i++) {
        html += '<button data-id="' + i + '" class="suggestions_switch_button"></button>'
    }
    document.querySelector('.suggestions_switch_buttons').innerHTML = html
}

main()
