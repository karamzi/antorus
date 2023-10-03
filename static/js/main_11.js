const usButton = document.getElementById('us')
const euButton = document.getElementById('eu')
const navLink = document.querySelectorAll('.nav_link')

const instance = axios.create({
    // baseURL: 'http://127.0.0.1:8000/',
    baseURL: 'https://antorus.com/',
})

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

function countCart(cart) {
    if (cart.coupon !== '' && cart.products.length > 0) {
        document.getElementById('coupon_name').innerText = 'Coupon: ' + cart.coupon
        document.querySelector('.coupon').style.display = 'flex'
        document.getElementById('coupon_price').innerHTML = cart.sign + ' - ' + cart.discount
    }
    document.getElementById('subtotal').innerText = cart.sign +  cart.subtotal
    document.getElementById('cart_total').innerText = cart.sign +  cart.total
}

function product_quantity(quantity) {
    document.getElementById('cart_count').innerText = quantity
}

if (navLink) {
    navLink.forEach(item => {
        item.addEventListener('click', function () {
            const nextSibling = this.nextSibling.nextSibling
            if (nextSibling.classList.contains('accordion') && nextSibling.style.display === 'none') {
                nextSibling.style.display = 'flex'
                this.classList.add('active')
                this.classList.add('open')
                // Анимация открытия подкатеглоий
                const countLength = nextSibling.querySelectorAll('a').length
                const height = countLength * 54 + 2
                let currentHeight = 0
                let counter = 0
                let open = setInterval(() => {
                    counter += 1
                    currentHeight += height / 20
                    nextSibling.style.height = currentHeight + 'px'
                    if (counter === 20) {
                        return clearInterval(open)
                    }
                }, 10)
            } else if (nextSibling.classList.contains('accordion') && nextSibling.style.display === 'flex') {
                const height = nextSibling.querySelectorAll('a').length * 54 + 2
                let currentHeight = height
                let counter = 0
                // Анимация закрытия подкатеглоий
                let close = setInterval(() => {
                    counter += 1
                    currentHeight -= height / 20
                    nextSibling.style.height = currentHeight + 'px'
                    if (counter === 20) {
                        nextSibling.style.display = 'none'
                        this.classList.remove('active')
                        this.classList.remove('open')
                        return clearInterval(close)
                    }
                }, 10)
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

const chatButtons = document.querySelectorAll('.chatButton')

if (chatButtons) {
    chatButtons.forEach(item => {
        item.addEventListener('click', () => {
            window.Tawk_API.maximize();
        })
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
const closeButton = document.querySelector('.mobile_menu_header')
const mobileMenu = document.querySelector('.mobile_menu')

burgerButton.addEventListener('click', () => {
    mobileMenu.classList.add('in')
})

closeButton.addEventListener('click', () => {
    mobileMenu.classList.remove('in')
})

const customOrderButton = document.getElementById('custom_order_button')

if (customOrderButton) {
    document.getElementById('chatButton').click()
}
