const usButton = document.getElementById('us')
const euButton = document.getElementById('eu')
const navLink = document.querySelectorAll('.nav_link')

usButton.addEventListener('click', function () {
    setCookie('us', 'currency')
    window.location.reload()
})
euButton.addEventListener('click', () => {
    setCookie('eu', 'currency')
    window.location.reload()
})

document.addEventListener('DOMContentLoaded', function () {
    if (currency === 'us') {
        euButton.classList.remove('active_currency')
        usButton.classList.add('active_currency')
    } else {
        usButton.classList.remove('active_currency')
        euButton.classList.add('active_currency')
    }
})

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    //baseURL: 'https://antorus.com/',
})

function countCart() {
    let cart
    let currencyTotal
    if (currency === 'us') {
        cart = getCookie('cartUs')
        currencyTotal = '$'
    } else {
        cart = getCookie('cartEu')
        currencyTotal = '€'
    }
    let subtotal = cart.reduce((sum, item) => sum + +item.total, 0)
    let total
    let coupon = getCookie('coupon')
    if (coupon && cart.length > 0) {
        let discount
        document.getElementById('coupon_name').innerText = 'Coupon: ' + coupon.name
        document.querySelector('.coupon').style.display = 'flex'
        discount = +coupon.discount / 100 * subtotal
        document.getElementById('coupon_price').innerHTML = '- ' + discount.toFixed(2)
        total = subtotal - discount
    } else {
        total = subtotal
    }
    total = total.toFixed(2)
    subtotal = subtotal.toFixed(2)
    document.getElementById('subtotal').innerText = currencyTotal + ' ' + subtotal
    document.getElementById('cart_total').innerText = currencyTotal + ' ' + total
}

function product_quantity() {
    if (currency === 'us') {
        document.getElementById('cart_count').innerText = getCookie('cartUs').length
    } else {
        document.getElementById('cart_count').innerText = getCookie('cartEu').length
    }
}

product_quantity()

if (navLink) {
    navLink.forEach(item => {
        item.addEventListener('click', function () {
            const nextSibling = this.nextSibling.nextSibling
            if (nextSibling.classList.contains('accordion') && nextSibling.style.display === 'none') {
                nextSibling.style.display = 'flex'
                this.classList.add('active')
                this.classList.add('open')
            } else if (nextSibling.classList.contains('accordion') && nextSibling.style.display === 'flex') {
                nextSibling.style.display = 'none'
                this.classList.remove('active')
                this.classList.remove('open')
            }
        })
    })
}

function getCookie(name) {
    let results = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)')
    if (name === 'csrftoken') {
        return results[2]
    }
    if ((name === 'coupon' || name === 'cookie_accepted') && !results) {
        return undefined
    }
    if (results) {
        return JSON.parse(results[2])
    } else
        return []
}


function setCookie(value, name) {
    let expires = ""
    let date = new Date()
    date.setTime(date.getTime() + (24 * 60 * 60 * 1000))
    expires = "; expires=" + date.toUTCString()
    document.cookie = name + "=" + (value || "") + expires + ";" + ' path=/;'
}

function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=0; path=/;'
}

const login = document.querySelector('.login')
const loginAccordion = document.querySelector('.login_accordion')
const account = document.querySelector('.account')
const accountAccordion = document.querySelector('.account_accordion')

if (login) {
    login.addEventListener('mouseover', function () {
        loginAccordion.style.display = 'block'
    })

    document.addEventListener('mousemove', function (e) {
        if (!e.target.closest('.login')) {
            loginAccordion.style.display = 'none'
        }
    })
}

if (account) {
    account.addEventListener('mouseover', function () {
        accountAccordion.style.display = 'flex'
    })

    document.addEventListener('mousemove', function (e) {
        if (!e.target.closest('.account')) {
            accountAccordion.style.display = 'none'
        }
    })
}

const searchBody = document.querySelector('.search_accordion')

function search() {
    const value = document.getElementById('search').value
    if (!value) {
        return
    }
    let data = new FormData()
    data.append('value', value)
    instance.post('searchProduct/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        searchBody.style.display = 'block'
        searchBody.innerHTML = response.data
    })
}

document.body.addEventListener('click', function (e) {
    if (!e.target.closest('.search_accordion')) {
        searchBody.style.display = 'none'
    }
})

const chatButton = document.getElementById('chatButton')

if (chatButton) {
    chatButton.addEventListener('click', () => {
        tidioChatApi.open()
    })
}

const contactSupport = document.getElementById('contact_support')
const modal = document.querySelector('.modal_container')

contactSupport.addEventListener('click', function () {
    modal.classList.add('modal_active')
    document.body.classList.add('body_modal')
})

document.body.addEventListener('click', function (e) {
    if (!e.target.closest('.modal_container') && !e.target.closest('#contact_support')) {
        modal.classList.remove('modal_active')
        document.body.classList.remove('body_modal')
    }
})

const cookie = document.getElementById('cookie')
const isCookieAccepted = getCookie('cookie_accepted')
const acceptCookie = document.getElementById('accept_cookie')

acceptCookie.addEventListener('click', function () {
    setCookie('true', 'cookie_accepted')
    cookie.style.display = 'none'
})

if (isCookieAccepted) {
    cookie.style.display = 'none'
} else {
    cookie.style.display = 'block'
}

const burgerButton = document.querySelector('.burger_button')
const closeButton = document.querySelector('.close_button')
const mobileMenu = document.querySelector('.mobile_menu')

burgerButton.addEventListener('click', () => {
    mobileMenu.classList.add('in')
})

closeButton.addEventListener('click', () => {
    mobileMenu.classList.remove('in')
})
