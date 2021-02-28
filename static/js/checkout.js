const button = document.querySelector('.button')
button.addEventListener('click', evt => createOrder(evt))

function renderCart() {
    const products = document.querySelector('.products')
    let cart
    if (currency === 'us') {
        cart = getCookie('cartUs')
    } else {
        cart = getCookie('cartEu')
    }
    let html = ''
    cart.forEach(item => {
        html += '<div class="product">' +
            '<div class="product_head">' +
            '<div class="product_name">' + item.name + ' x ' + item.quantity + '</div>' +
            '<div class="product_price">' + item.currency + ' ' + item.total + '</div>' +
            '</div>' +
            '<div class="product_options">'

        item.options.forEach(item => {
            html += '<div class="options">Select options: ' + item.name + '</div>'
        })

        html += '</div>' +
            '</div>'
    })
    products.innerHTML = html
    countCart()
}

function createOrder(e) {
    e.preventDefault()
    const characterServer = document.getElementById('characterServer').value
    const battleTag = document.getElementById('battleTag').value
    const faction = document.getElementById('faction').value
    const connection = document.getElementById('connection').value
    const email = document.getElementById('email').value
    const account = document.getElementById('cd1').checked
    const comment = document.getElementById('comment').value
    let cart
    let total
    let coupon = getCookie('coupon')
    if (currency === 'us') {
        cart = getCookie('cartUs')
    } else {
        cart = getCookie('cartEu')
    }
    if (!characterServer && !faction && !connection && !email || cart.length === 0) {
        return
    }
    total = cart.reduce((sum, item) => sum + +item.total, 0)
    cart = JSON.stringify(cart)
    let data = new FormData()
    if (coupon) {
        let discount
        discount = +coupon.discount / 100 * total
        data.append('oldPrice', total.toFixed(2))
        data.append('coupon', coupon.name)
        total = total - discount
    }
    total = total.toFixed(2)
    data.append('cart', cart)
    data.append('total', total)
    data.append('currency', currency)
    data.append('characterServer', characterServer)
    data.append('battleTag', battleTag)
    data.append('faction', faction)
    data.append('connection', connection)
    data.append('email', email)
    data.append('account', account)
    data.append('comment', comment)
    instance.post('createOrder/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {})
}

renderCart()