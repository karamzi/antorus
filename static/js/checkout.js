const button = document.querySelector('.button')
button.addEventListener('click', createOrder)

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

function createOrder() {
    const characterServer = document.getElementById('characterServer')
    const battleTag = document.getElementById('battleTag').value
    const faction = document.getElementById('faction')
    const connection = document.getElementById('connection')
    const email = document.getElementById('email')
    //const account = document.getElementById('cd1').checked
    const comment = document.getElementById('comment').value
    let cart
    let total
    let coupon = getCookie('coupon')
    if (currency === 'us') {
        cart = getCookie('cartUs')
    } else {
        cart = getCookie('cartEu')
    }
    if (!checkForm(characterServer, faction, connection, email) || cart.length === 0) {
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
    data.append('characterServer', characterServer.value)
    data.append('battleTag', battleTag)
    data.append('faction', faction.value)
    data.append('connection', connection.value)
    data.append('email', email.value)
    data.append('account', account)
    data.append('comment', comment)
    instance.post('createOrder/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        data = response.data
        document.getElementById('amount').value = data['amount']
        document.getElementById('currency').value = data['currency']
        document.getElementById('order_desc').value = data['order_desc']
        document.getElementById('order_id').value = data['order_id']
        document.getElementById('signature').value = data['signature']
        eraseCookie('cartEu')
        eraseCookie('cartUs')
        eraseCookie('coupon')
        document.getElementById('fondy').submit()
    })
}

function checkForm(characterServer, faction, connection, email) {
    characterServer.classList.remove('input_error')
    faction.classList.remove('input_error')
    connection.classList.remove('input_error')
    email.classList.remove('input_error')
    if (checkInput(characterServer)) return false
    if (checkInput(faction)) return false
    if (checkInput(connection)) return false
    if (checkInput(email)) return false
    if (!checkEmail(email)) return false
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

function checkEmail(email) {
    let regexEmail = new RegExp('^[\\w]{1}[\\w-\\.]*@[\\w-]+\\.[a-z]{2,4}$')
    if (regexEmail.test(email.value)) {
        return true
    }
    email.classList.add('input_error')
    return false
}

renderCart()