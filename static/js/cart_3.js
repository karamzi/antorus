const inputButton = document.querySelector('.input_button')
let minus = document.querySelector('.minus')
let plus = document.querySelector('.plus')

inputButton.addEventListener('click', checkCoupon)

function renderCart(cart = undefined) {
    const products = document.querySelector('.cart_products')
    let sing
    if (currency === 'us') {
        sing = '$'
    } else {
        sing = '€'
    }
    if (!cart.products.length) {
        document.querySelector('.cart_content').style.display = 'none'
        document.querySelector('.cart_empty').style.display = 'flex'
        return
    }
    let html = ''
    cart.products.forEach(item => {
        html += '<div class="product" data-id="' + item.id + '">' +
            '<div class="product_description">' +
            '<img src="' + item.image + '" alt="">' +
            '<div class="description">' +
            '<div class="product_name"><a href="' + item.url + '">' + item.name + '</a></div>' +
            '<div class="product_options">' +
            '<h4>Options</h4>'
        item.options.forEach(item => {
            html += '<p>Select options: ' + item.name + '</p>'
        })
        html += '<span class="removeFromCart">Remove</span>' +
            '<div class="mobile_cart">' +
            '<div class="price mobile">' + sing + ' ' + item.price + '</div>' +
            '<div class="product_quantity mobile">' +
            '<div class="quantity mobile">' +
            '<div class="minus"></div>' +
            '<div class="count">' + item.quantity + '</div>' +
            '<div class="plus">+</div>' +
            '</div>' +
            '</div>' +
            '<div class="total mobile">' + sing + ' ' + item.total + '</div>' +
            '</div>'
        html += '</div>' +
            '</div>' +
            '</div>' +
            '<div class="price">' + sing + ' ' + item.price + '</div>' +
            '<div class="product_quantity">' +
            '<div class="quantity">' +
            '<div class="minus"></div>' +
            '<div class="count">' + item.quantity + '</div>' +
            '<div class="plus">+</div>' +
            '</div>' +
            '</div>' +
            '<div class="total">' + sing + ' ' + item.total + '</div>' +
            '</div>'
    })
    products.innerHTML = html
    countCart(cart)
    setup()
}

function setup() {
    minus = document.querySelectorAll('.minus')
    plus = document.querySelectorAll('.plus')
    const removeFromCartButton = document.querySelectorAll('.removeFromCart')

    minus && minus.forEach(item => item.addEventListener('click', setPrice))
    plus && plus.forEach(item => item.addEventListener('click', setPrice))
    removeFromCartButton && removeFromCartButton.forEach(item => item.addEventListener('click', removeFromCart))
}

function setPrice() {
    changeButtons(this)
}

function changeButtons(pressedButton) {
    let productId
    let quantity
    let count = pressedButton.closest('.product').querySelector('.count')
    let product = pressedButton.closest('.product')
    plus.forEach(item => {
        if (pressedButton === item) {
            productId = product.getAttribute('data-id')
            quantity = +product.querySelector('.count').innerText + 1
        }
    })
    minus.forEach(item => {
        if (pressedButton === item && +count.innerText > 1) {
            productId = product.getAttribute('data-id')
            quantity = +product.querySelector('.count').innerText - 1
        }
    })
    let data = {
        'action': 'change',
        'productId': productId,
        'quantity': quantity,
    }
    instance.post('cartService/', data, {
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        product_quantity(response.data.products.length)
        renderCart(response.data)
    })
}

function checkCoupon() {
    const coupon = document.getElementById('coupon').value
    const messageError = document.getElementById('couponNotFound')
    messageError.style.display = 'none'
    if (!coupon) {
        return
    }
    let data = new FormData()
    data.append('coupon', coupon)
    instance.post('checkCoupon/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        console.log(response.data.status)
        if (response.data.status) {
            countCart(response.data.cart)
        } else {
            messageError.style.display = 'block'
        }
    })
}

function removeFromCart() {
    const productId = this.closest('.product').getAttribute('data-id')
    let data = {
        'action': 'remove',
        'productId': productId,
    }
    instance.post('cartService/', data, {
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        product_quantity(response.data.products.length)
        renderCart(response.data)
    })
}

setup()
