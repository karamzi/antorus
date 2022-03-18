class SpecialOffersSlider {
    left_button = document.querySelector('.slider_arrow.left')
    right_button = document.querySelector('.slider_arrow.right')
    sections = document.querySelectorAll('.special_offers_item')
    slider = document.querySelector('.special_offers_items')
    max_slides = 0
    id = 0
    move = 0
    touchStartPosition = 0

    constructor() {
        this.right_button.addEventListener('click', () => this.switch_slide_right())
        this.left_button.addEventListener('click', () => this.switch_slide_left())
        this.moveHendler = this.moveSlider.bind(this)
        this.sections.forEach(item => item.addEventListener('touchstart', event => {
            this.touchStartPosition = event.touches[0].clientX
            window.addEventListener('touchmove', this.moveHendler)
        }))
        window.addEventListener('resize', () => this.set_slider())
        this.set_slider()
    }

    set_slider() {
        const arrows = document.querySelectorAll('.slider_arrow')
        if (window.innerWidth > 900) {
            this.sections.length > 3 ? arrows.forEach(item => item.style.display = 'block') : arrows.forEach(item => item.style.display = 'none')
            this.max_slides = this.sections.length - 3
            this.move = 33.33333
            this.sections.forEach(item => item.style.minWidth = '33.33333%')
        } else if (window.innerWidth > 650 && window.innerWidth <= 900) {
            this.sections.length > 2 ? arrows.forEach(item => item.style.display = 'block') : arrows.forEach(item => item.style.display = 'none')
            this.max_slides = this.sections.length - 2
            this.move = 50
            this.sections.forEach(item => item.style.minWidth = '50%')
        } else if (window.innerWidth <= 650) {
            this.sections.length > 1 ? arrows.forEach(item => item.style.display = 'block') : arrows.forEach(item => item.style.display = 'none')
            this.max_slides = this.sections.length - 1
            this.move = 100
            this.sections.forEach(item => item.style.minWidth = '100%')
        }
    }

    switch_slide_left() {
        this.decrease_id()
        this.slider.style.transform = 'translateX(' + -this.move * this.id + '%)'
    }

    switch_slide_right() {
        this.increase_id()
        this.slider.style.transform = 'translateX(' + -this.move * this.id + '%)'
    }

    moveSlider(event) {
        let difference = event.touches[0].clientX - this.touchStartPosition
        if (difference < -70) {
            window.removeEventListener('touchmove', this.moveHendler)
            this.switch_slide_right()
        }

        if (difference > 70) {
            window.removeEventListener('touchmove', this.moveHendler)
            this.switch_slide_left()
        }
    }

    increase_id() {
        if (this.id === this.max_slides) {
            this.id = 0
        } else {
            this.id += 1
        }
    }

    decrease_id() {
        if (this.id === 0) {
            this.id = this.max_slides
        } else {
            this.id -= 1
        }
    }
}

new SpecialOffersSlider()
