let minus = document.querySelector('.minus')
let plus = document.querySelector('.plus')
let count = document.querySelector('.count')


function renderCart() {
    const products = document.querySelector('.products')
    let cart = getCookie('cart')
    let html = ''
    cart.forEach(item => {
        html += '<div class="product" data-id="' + item.id + '">' +
            '<div class="product_description">' +
            '<img src="' + item.image + '" alt="">' +
            '<div class="description">' +
            '<div class="product_name"><a href="">' + item.name + '</a></div>' +
            '<div class="product_options">' +
            '<h4>Options</h4>'

        item.options.forEach(item => {
            html += '<p>Select options: ' + item + '</p>'
        })

        html += '</div>' +
            '</div>' +
            '</div>' +
            '<div class="price">' + item.price + '</div>' +
            '<div class="product_quantity">' +
            '<div class="quantity">' +
            '<div class="minus"></div>' +
            '<div class="count">' + item.quantity + '</div>' +
            '<div class="plus">+</div>' +
            '</div>' +
            '</div>' +
            '<div class="total">' + item.total + '</div>' +
            '</div>'
    })
    products.innerHTML = html

    minus = document.querySelectorAll('.minus')
    plus = document.querySelectorAll('.plus')
    count = document.querySelector('.count')

    minus && minus.forEach(item => item.addEventListener('click', setPrice))
    plus && plus.forEach(item => item.addEventListener('click', setPrice))
    countCart()
}

function setPrice() {
    let cart = getCookie('cart')
    plus.forEach(item => {
        if (this === item) {
            let id = this.closest('.product').getAttribute('data-id')
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
        if (this === item && +count.innerText > 1) {
            let id = this.closest('.product').getAttribute('data-id')
            cart.forEach(item => {
                if (item.id === id) {
                    item.quantity = +item.quantity - 1
                    item.total = item.price * item.quantity
                    item.total = item.total.toFixed(2)
                }
            })
        }
    })

    cart = JSON.stringify(cart)
    setCookie(cart, 'cart')
    renderCart()
}

function countCart() {
    const cart = getCookie('cart')
    let total = cart.reduce((sum, item) => sum + +item.total, 0)
    document.getElementById('subtotal').innerText = '€ ' + total
    document.getElementById('cart_total').innerText = '€ ' + total
}

renderCart()