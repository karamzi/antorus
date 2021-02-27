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
            '<div class="product_name">'+ item.name + ' x ' + item.quantity + '</div>' +
            '<div class="product_price">'+ item.currency + ' ' + item.total +'</div>' +
            '</div>' +
            '<div class="product_options">'

        item.options.forEach(item => {
            html += '<div class="options">Select options: '+ item +'</div>'
        })

        html += '</div>' +
            '</div>'
    })
    products.innerHTML = html
    countCart()
}

renderCart()