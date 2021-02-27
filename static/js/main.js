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
    //baseURL: 'https://bowling-petersburg.ru/api/1.0/',
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
    let total = cart.reduce((sum, item) => sum + +item.total, 0)
    total = total.toFixed(2)
    document.getElementById('subtotal').innerText = currencyTotal + ' ' + total
    document.getElementById('cart_total').innerText = currencyTotal + ' ' + total
}


function getCookie(name) {
    let results = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)')
    if (name === 'csrftoken') {
        return results[2]
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