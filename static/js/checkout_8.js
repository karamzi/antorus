const button = document.querySelector('.button')
button.addEventListener('click', createOrder)

function renderCart() {
    const products = document.querySelector('.products')
    let cart
    let sing
    if (currency === 'us') {
        cart = getCookie('cartUs')
        sing = '$'
    } else {
        cart = getCookie('cartEu')
        sing = '€'
    }
    let html = ''
    cart.forEach(item => {
        html += '<div class="product">' +
            '<div class="product_head">' +
            '<div class="product_name">' + item.name + ' x ' + item.quantity + '</div>' +
            '<div class="product_price">' + sing + ' ' + item.total + '</div>' +
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

function createOrder() {
    const connection = document.getElementById('connection')
    const email = document.getElementById('email')
    const comment = document.getElementById('comment').value
    let cart
    let total
    let coupon = getCookie('coupon')
    if (currency === 'us') {
        cart = getCookie('cartUs')
    } else {
        cart = getCookie('cartEu')
    }
    if (!checkForm(connection, email) || cart.length === 0) {
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
    data.append('connection', connection.value)
    data.append('email', email.value)
    data.append('comment', comment)
    button.querySelector('button').setAttribute('disabled', 'disabled')
    instance.post('createOrder/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        if (response.status === 200) {
            data = response.data
            document.getElementById('amount').value = data['amount']
            document.getElementById('currency').value = data['currency']
            document.getElementById('order_desc').value = data['order_desc']
            document.getElementById('order_id').value = data['order_id']
            document.getElementById('signature').value = data['signature']
            document.getElementById('fondy').submit()
            ym(67968427,'reachGoal','order')
        }
        button.querySelector('button').removeAttribute('disabled')
    })
}

function checkForm(connection, email) {
    connection.classList.remove('input_error')
    email.classList.remove('input_error')
    if (checkInput(connection)) return false
    if (checkInput(email)) return false
    const agreeInput = document.getElementById('cd2')
    const label = document.getElementById('cd2_label')
    label.style.color = 'rgb(136, 136, 136)'
    if (!agreeInput.checked) {
        label.style.color = 'darkred'
        return false
    }
    return true
}

function checkInput(input) {
    if (input.value === '') {
        input.classList.add('input_error')
        return false
    }
}

renderCart()