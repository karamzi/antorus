const requiredInputs = document.querySelectorAll('.required.parent')
const requiredChildInputs = document.querySelectorAll('.required.child')
const additionInputs = document.querySelectorAll('.addition')
const options = document.querySelectorAll('.option_name')
const minus = document.querySelector('.minus')
const plus = document.querySelector('.plus')
const count = document.querySelector('.count')
const addToCartButton = document.querySelector('.add_to_cart')
let requiredChecked = []
let requiredChildChecked = []
let additionChecked = []
let priceUs = 0
let priceEu = 0

minus.addEventListener('click', setPrice)
plus.addEventListener('click', setPrice)
addToCartButton.addEventListener('click', addToCart)

if (requiredInputs) {
    checkInputs(requiredInputs, quantityRequiredOptions, requiredChecked)
}

if (additionChecked) {
    checkInputs(additionInputs, quantityAdditionOptions, additionChecked)
}

if (requiredChildInputs) {
    checkInputs(requiredChildInputs, quantityRequiredChildOptions, requiredChildChecked)
}

function checkInputs(inputs, max, array) {
    inputs.forEach(item => {
        item.addEventListener('change', function () {
            if (this.checked && (array.length < max || !max)) {
                array.push(this)
                showChildOptions(this)
            } else if (this.checked && array.length.toString() === max) {
                array.push(this)
                showChildOptions(this)
                let input = array.shift()
                input.checked = false
                hideChildOptions(input)
            } else {
                array.forEach((item, index, array) => {
                    if (item === this) {
                        array.splice(index, 1)
                        hideChildOptions(this)
                    }
                })
            }
            countAdditionOptionsPrice()
            setPrice()
        })
    })
}

function countAdditionOptionsPrice() {
    let sing
    currency === 'us' ? sing = '$' : sing = '€'
    let amountRequirementOptions = 0
    requiredChecked.forEach(item => {
        let price
        currency === 'us' ? price = item.closest('.option').getAttribute('data-price-us') : price = item.closest('.option').getAttribute('data-price-eu')
        price = price.replace(',', '.')
        amountRequirementOptions += +price
    })

    if (amountRequirementOptions > 0) {
        additionInputs.forEach(item => {
            const option = item.closest('.option')
            let percent
            currency === 'us' ? percent = option.getAttribute('data-percent-us') : percent = option.getAttribute('data-percent-eu')
            if (percent) {
                percent = percent.replace(',', '.')
                let amount = amountRequirementOptions * +percent
                currency === 'us' ? option.setAttribute('data-price-us', amount.toFixed(2)) : option.setAttribute('data-price-eu', amount.toFixed(2))
                option.querySelector('.option_price').innerText = sing + ' ' + amount.toFixed(2)
            }
        })
    } else {
        additionInputs.forEach((item, index, array) => {
            const option = item.closest('.option')
            let percent
            currency === 'us' ? percent = option.getAttribute('data-percent-us') : percent = option.getAttribute('data-percent-eu')
            if (percent) {
                item.closest('.option').querySelector('.option_price').innerText = ''
                currency === 'us' ? option.setAttribute('data-price-us', '') : option.setAttribute('data-price-eu', '')
                item.checked = false
                Array.prototype.slice.call(array).splice(index, 1)
            }
        })
        additionChecked.splice(0, additionChecked.length)
    }
}

function showChildOptions(option) {
    const option_id = option.closest('.option').getAttribute('data-id')
    if (option_id) {
        requiredChildInputs.forEach(item => {
            const parentId = item.closest('.option').getAttribute('data-parent-id')
            if (parentId === option_id) {
                item.closest('.child_option').style.display = 'block'
            }
        })
    }
}

function hideChildOptions(option) {
    const option_id = option.closest('.option').getAttribute('data-id')
    if (option_id) {
        requiredChildInputs.forEach((item, index, array) => {
            const parentId = item.closest('.option').getAttribute('data-parent-id')
            if (parentId === option_id) {
                item.closest('.child_option').style.display = 'none'
                item.checked = false
                Array.prototype.slice.call(array).splice(index, 1)
            }
        })
    }
}

function setPrice() {
    const priceHtml = document.querySelector('.price').querySelector('p')
    priceUs = 0
    priceEu = 0
    priceUs += +productPriceUs.replace(',', '.')
    priceEu += +productPriceEu.replace(',', '.')
    requiredChecked.forEach(item => {
        priceUs += +item.closest('.option').getAttribute('data-price-us').replace(',', '.')
        priceEu += +item.closest('.option').getAttribute('data-price-eu').replace(',', '.')
    })
    requiredChildChecked.forEach(item => {
        priceUs += +item.closest('.option').getAttribute('data-price-us').replace(',', '.')
        priceEu += +item.closest('.option').getAttribute('data-price-eu').replace(',', '.')
    })
    additionChecked.forEach(item => {
        priceUs += +item.closest('.option').getAttribute('data-price-us').replace(',', '.')
        priceEu += +item.closest('.option').getAttribute('data-price-eu').replace(',', '.')
    })
    if (this === plus) {
        count.innerText = +count.innerHTML + 1
    }
    if (this === minus && +count.innerText > 1) {
        count.innerText = +count.innerHTML - 1
    }
    let quantity = +count.innerText
    priceUs = priceUs * quantity
    priceEu = priceEu * quantity
    if (currency === 'us' && priceUs > 0) {
        priceHtml.innerText = '$ ' + ' ' + priceUs.toFixed(2)
    } else if (currency === 'us' && priceUs === 0) {
        priceHtml.innerHTML = '<p>Choose options to continue</p>'
    } else if (currency === 'eu' && priceEu > 0) {
        priceHtml.innerText = '€ ' + ' ' + priceEu.toFixed(2)
    } else if (currency === 'eu' && priceEu === 0) {
        priceHtml.innerHTML = '<p>Choose options to continue</p>'
    }
}

function generateProductObject(price, region) {
    let product = {}
    product['name'] = name
    product['url'] = url
    product['total'] = price.toFixed(2)
    product['quantity'] = count.innerText
    product['price'] = product.total / product.quantity
    product.price = product.price.toFixed(2)
    product['image'] = imgURL
    product['id'] = productId
    product['options'] = []
    requiredChecked.forEach(input => {
        product.options.push(generateOptionObject(input, region))
    })
    additionChecked.forEach(input => {
        product.options.push(generateOptionObject(input, region))
    })
    requiredChildChecked.forEach(input => {
        product.options.push(generateOptionObject(input, region))
    })
    return product
}

function generateOptionObject(input, region) {
    let item = {}
    item['name'] = input.closest('.option').getAttribute('data-name')
    if (region === 'us') {
        item['price'] = input.closest('.option').getAttribute('data-price-us')
    } else {
        item['price'] = input.closest('.option').getAttribute('data-price-eu')
    }
    return item
}

function addToCart() {
    const notificationSuccess = document.querySelector('.success')
    const notificationError = document.querySelector('.error')
    if (requiredInputs.length > 0 && requiredChecked.length === 0) {
        notificationError.style.display = 'block'
        setTimeout(function () {
            notificationError.style.display = 'none'
        }, 2500)
        return
    }
    if (childIsRequired === 'True' && requiredChildChecked.length === 0) {
        notificationError.style.display = 'block'
        setTimeout(function () {
            notificationError.style.display = 'none'
        }, 2500)
        return
    }
    let productUs = generateProductObject(priceUs, 'us')
    let productEu = generateProductObject(priceEu, 'eu')
    productUs['currency'] = '$'
    productEu['currency'] = '€'
    let cartUs = getCookie('cartUs')
    let cartEu = getCookie('cartEu')
    cartUs.forEach((item, index, array) => {
        if (item.id === productUs.id) {
            array.splice(index, 1)
        }
    })
    cartEu.forEach((item, index, array) => {
        if (item.id === productEu.id) {
            array.splice(index, 1)
        }
    })
    cartUs.push(productUs)
    cartEu.push(productEu)
    cartUs = JSON.stringify(cartUs)
    cartEu = JSON.stringify(cartEu)
    setCookie(cartUs, 'cartUs')
    setCookie(cartEu, 'cartEu')
    product_quantity()
    notificationSuccess.style.display = 'block'
    setTimeout(function () {
        notificationSuccess.style.display = 'none'
    }, 2500)
}

const questions = document.querySelectorAll('.hint_img')
let intervalID

if (questions) {
    questions.forEach(item => {
        item.addEventListener('mouseover', function () {
            clearInterval(intervalID)
            this.nextSibling.nextSibling.querySelector('.hint_text').style.display = 'block'
            this.nextSibling.nextSibling.querySelector('.hint_text').classList.add('hint_active')
        })
    })

    questions.forEach(item => {
        item.addEventListener('mouseleave', function () {
            this.nextSibling.nextSibling.querySelector('.hint_text').classList.remove('hint_active')
            intervalID = setTimeout(() => {
                this.nextSibling.nextSibling.querySelector('.hint_text').style.display = 'none'
            }, 500)
        })
    })
}


options.forEach(item => {
    item.addEventListener('click', function () {
        const input = this.closest('.option').querySelector('input')
        input.click()
    })
})

window.addEventListener("pageshow", function (event) {
    let historyTraversal = event.persisted ||
        (typeof window.performance != "undefined" &&
            window.performance.navigation.type === 2);
    if (historyTraversal) {
        window.location.reload();
    }
})
