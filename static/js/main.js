const usButton = document.getElementById('us')
const euButton = document.getElementById('eu')
const navLink = document.querySelectorAll('.nav_link')

usButton.addEventListener('click', () => {
    setCookie('us', 'currency')
    window.location.reload()
})
euButton.addEventListener('click', () => {
    setCookie('eu', 'currency')
    window.location.reload()
})

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    //baseURL: 'http://151.248.114.152/',
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
        document.getElementById('coupon_price').innerHTML = '- ' + discount.toFixed(2) + ' <span class="coupon_remove">Remove</span>'
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
    if (name === 'coupon' && !results) {
        return undefined
    }
    if (results)
        return JSON.parse(unescape(results[2]))
    else
        return []
}


function setCookie(value, name) {
    let expires = ""
    let date = new Date()
    date.setTime(date.getTime() + (90 * 1000))
    expires = "; expires=" + date.toUTCString()
    document.cookie = name + "=" + (value || "") + expires + ";" + ' path=/;'
}

function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999;';
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
