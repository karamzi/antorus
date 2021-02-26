const requiredInputs = document.querySelectorAll('.required')
const additionInputs = document.querySelectorAll('.addition')
const options = document.querySelectorAll('.option_name')
const minus = document.querySelector('.minus')
const plus = document.querySelector('.plus')
const count = document.querySelector('.count')
const addToCartButton = document.querySelector('.add_to_cart')
let requiredChecked = []
let additionChecked = []
let price = 0

minus.addEventListener('click', setPrice)
plus.addEventListener('click', setPrice)
addToCartButton.addEventListener('click', addToCart)

if (requiredInputs) {
    checkInputs(requiredInputs, quantityRequiredOptions, requiredChecked)
}

if (additionChecked) {
    checkInputs(additionInputs, quantityAdditionOptions, additionChecked)
}

function checkInputs(inputs, max, array) {
    inputs.forEach(item => {
        item.addEventListener('change', function () {
            if (this.checked && (array.length < max || !max)) {
                array.push(this)
            } else if (this.checked && array.length.toString() === max) {
                array.push(this)
                array.shift().checked = false
            } else {
                array.forEach((item, index, array) => {
                    if (item === this) {
                        array.splice(index, 1)
                    }
                })
            }
            setPrice()
        })
    })
}

function setPrice() {
    const priceHtml = document.querySelector('.price').querySelector('p')
    price = 0
    price += +productPrice.replace(',', '.')
    requiredChecked.forEach(item => {
        price += +item.closest('.option').getAttribute('data-price').replace(',', '.')
    })
    additionChecked.forEach(item => {
        price += +item.closest('.option').getAttribute('data-price').replace(',', '.')
    })
    if (this === plus) {
        count.innerText = +count.innerHTML + 1
    }
    if (this === minus && +count.innerText > 1) {
        count.innerText = +count.innerHTML - 1
    }
    let quantity = +count.innerText
    price = price * quantity
    priceHtml.innerText = currencySign + price.toFixed(2)
}

function generateProductObject() {
    let product = {}
    product['name'] = name
    product['total'] = price
    product['quantity'] = count.innerText
    product['price'] = product.total / product.quantity
    product['options'] = []
    requiredChecked.forEach(input => {
        product.options.push(generateOptionObject(input))
    })
    additionChecked.forEach(input => {
        product.options.push(generateOptionObject(input))
    })
    return product
}

function generateOptionObject(input) {
    let item = {}
    item['name'] = input.closest('.option').getAttribute('data-name')
    item['price'] = input.closest('.option').getAttribute('data-price')
    return item
}

function addToCart() {
    let product = generateProductObject()
    let cart = getCookie('cart')
    cart.push(product)
    cart = JSON.stringify(cart)
    setCookie(cart, 'cart')
}

options.forEach(item => {
    item.addEventListener('click', function () {
        const input = this.closest('.option').querySelector('input')
        input.click()
    })
})
