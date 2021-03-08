const inputButton = document.querySelector('.input_button')
let minus = document.querySelector('.minus')
let plus = document.querySelector('.plus')
let count = document.querySelector('.count')

inputButton.addEventListener('click', checkCoupon)

function renderCart() {
    const products = document.querySelector('.products')
    let cart
    if (currency === 'us') {
        cart = getCookie('cartUs')
    } else {
        cart = getCookie('cartEu')
    }
    if (!cart.length) {
        document.querySelector('.cart_content').style.display = 'none'
        document.querySelector('.cart_empty').style.display = 'flex'
        return
    }
    let html = ''
    cart.forEach(item => {
        console.log(item)
        html += '<div class="product" data-id="' + item.id + '">' +
            '<div class="product_description">' +
            '<img src="' + item.image + '" alt="">' +
            '<div class="description">' +
            '<div class="product_name"><a href="'+ item.url +'">' + item.name + '</a></div>' +
            '<div class="product_options">' +
            '<h4>Options</h4>'
        item.options.forEach(item => {
            html += '<p>Select options: ' + item.name + '</p>'
        })
        html += '<span class="removeFromCart">Remove</span>'+
            '<div class="mobile_cart">'+
            '<div class="price mobile">' + item.currency + ' ' + item.price + '</div>' +
            '<div class="product_quantity mobile">' +
            '<div class="quantity mobile">' +
            '<div class="minus"></div>' +
            '<div class="count">' + item.quantity + '</div>' +
            '<div class="plus">+</div>' +
            '</div>' +
            '</div>' +
            '<div class="total mobile">' + item.currency + ' ' + item.total + '</div>'+
            '</div>'
        html += '</div>' +
            '</div>' +
            '</div>' +
            '<div class="price">' + item.currency + ' ' + item.price + '</div>' +
            '<div class="product_quantity">' +
            '<div class="quantity">' +
            '<div class="minus"></div>' +
            '<div class="count">' + item.quantity + '</div>' +
            '<div class="plus">+</div>' +
            '</div>' +
            '</div>' +
            '<div class="total">' + item.currency + ' ' + item.total + '</div>' +
            '</div>'
    })
    products.innerHTML = html

    minus = document.querySelectorAll('.minus')
    plus = document.querySelectorAll('.plus')
    count = document.querySelector('.count')
    const removeFromCartButton = document.querySelectorAll('.removeFromCart')

    minus && minus.forEach(item => item.addEventListener('click', setPrice))
    plus && plus.forEach(item => item.addEventListener('click', setPrice))
    removeFromCartButton && removeFromCartButton.forEach(item => item.addEventListener('click', removeFromCart))
    countCart()
}

function setPrice() {
    let cartUs = getCookie('cartUs')
    let cartEu = getCookie('cartEu')
    cartUs = changeButtons(cartUs, this)
    cartEu = changeButtons(cartEu, this)
    cartUs = JSON.stringify(cartUs)
    setCookie(cartUs, 'cartUs')
    cartEu = JSON.stringify(cartEu)
    setCookie(cartEu, 'cartEu')
    renderCart()
}

function changeButtons(cart, pressedButton) {
    plus.forEach(item => {
        if (pressedButton === item) {
            let id = pressedButton.closest('.product').getAttribute('data-id')
            cart.forEach(item => {
                if (item.id === id) {
                    item.quantity = +item.quantity + 1
                    item.total = item.price * item.quantity
                    item.total = item.total.toFixed(2)
                }
            })
        }
    })
    minus.forEach(item => {
        if (pressedButton === item && +count.innerText > 1) {
            let id = pressedButton.closest('.product').getAttribute('data-id')
            cart.forEach(item => {
                if (item.id === id) {
                    item.quantity = +item.quantity - 1
                    item.total = item.price * item.quantity
                    item.total = item.total.toFixed(2)
                }
            })
        }
    })
    return cart
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
    instance.post('checkCoupon/', data,  {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        if (response.data.status === 'True') {
            let discount = {
                'name': response.data.name,
                'discount': response.data.discount,
            }
            discount = JSON.stringify(discount)
            setCookie(discount, 'coupon')
            countCart()
        } else if (response.data.status === 'False') {
            messageError.style.display = 'block'
        }
    })
}

function removeFromCart() {
    const productId = this.closest('.product').getAttribute('data-id')
    let cartUs = getCookie('cartUs')
    let cartEu = getCookie('cartEu')
    cartUs.forEach((item, index, array) => {
        if (item.id === productId) {
            array.splice(index, 1)
        }
    })
    cartEu.forEach((item, index, array) => {
        if (item.id === productId) {
            array.splice(index, 1)
        }
    })
    cartUs = JSON.stringify(cartUs)
    cartEu = JSON.stringify(cartEu)
    setCookie(cartUs, 'cartUs')
    setCookie(cartEu, 'cartEu')
    renderCart()
}

renderCart()