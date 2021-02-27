const usButton = document.getElementById('us')
const euButton = document.getElementById('eu')

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
    //baseURL: '',
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
    document.cookie = name+'=; Max-Age=-99999999;';
}