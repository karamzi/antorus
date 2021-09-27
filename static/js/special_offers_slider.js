class SpecialOffersSlider {
    left_button = document.querySelector('.slider_arrow.left')
    right_button = document.querySelector('.slider_arrow.right')
    sections = document.querySelectorAll('.intro_section')
    id = 0

    constructor() {
        this.left_button.addEventListener('click', this.switch_slide_left)
        this.right_button.addEventListener('click', this.switch_slide_right)
    }

    switch_slide_left() {
        const slider = document.querySelector('.special_offers_items')
        slider.style.transform = 'translateX(' + 0 + '%)'
    }

    switch_slide_right() {
        const slider = document.querySelector('.special_offers_items')
        slider.style.transform = 'translateX(' + -33 + '%)'
    }

    get_id() {

    }
}

new SpecialOffersSlider()
