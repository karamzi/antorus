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

minus && minus.addEventListener('click', setPrice)
plus && plus.addEventListener('click', setPrice)
addToCartButton && addToCartButton.addEventListener('click', addToCart)

if (requiredInputs) {
    checkInputs(requiredInputs, quantityRequiredOptions, requiredChecked)
}

if (additionInputs) {
    // search for default checked inputs
    additionInputs.forEach(item => {
        if (item.checked) {
            additionChecked.push(item)
        }
    })
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
            if ((document.querySelector('.option[data-percent-us]') && currency === 'us') || (document.querySelector('.option[data-percent-eu]') && currency === 'eu')) {
                countAdditionOptionsPrice()
            }
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
            }
        })

        for (let i = requiredChildChecked.length - 1; i >= 0; i--) {
            const parentId = requiredChildChecked[i].closest('.option').getAttribute('data-parent-id')
            if (parentId === option_id) {
                requiredChildChecked.splice(i, 1)
            }
        }
    }
}

function setPrice() {
    const priceHtml = document.getElementById('price')
    priceUs = 0
    priceEu = 0
    if (currency === 'us') {
        priceUs += +productPriceUs.replace(',', '.')
        requiredChecked.forEach(item => {
            priceUs += +item.closest('.option').getAttribute('data-price-us').replace(',', '.')
        })
        requiredChildChecked.forEach(item => {
            priceUs += +item.closest('.option').getAttribute('data-price-us').replace(',', '.')
        })
        additionChecked.forEach(item => {
            priceUs += +item.closest('.option').getAttribute('data-price-us').replace(',', '.')
        })
    }

    if (currency === 'eu') {
        priceEu += +productPriceEu.replace(',', '.')
        requiredChecked.forEach(item => {
            priceEu += +item.closest('.option').getAttribute('data-price-eu').replace(',', '.')
        })
        requiredChildChecked.forEach(item => {
            priceEu += +item.closest('.option').getAttribute('data-price-eu').replace(',', '.')
        })
        additionChecked.forEach(item => {
            priceEu += +item.closest('.option').getAttribute('data-price-eu').replace(',', '.')
        })
    }


    if (this === plus) {
        count.innerText = +count.innerHTML + 1
    }
    if (this === minus && +count.innerText > 1) {
        count.innerText = +count.innerHTML - 1
    }
    let quantity = +count.innerText

    if (currency === 'us') {
        priceUs = priceUs * quantity
        if (priceUs > 0) {
            priceHtml.innerText = '$ ' + ' ' + priceUs.toFixed(2)
        } else if (priceUs === 0) {
            priceHtml.innerHTML = '<p>Choose options to continue</p>'
        }
    }
    if (currency === 'eu') {
        priceEu = priceEu * quantity
        if (priceEu > 0) {
            priceHtml.innerText = '€ ' + ' ' + priceEu.toFixed(2)
        } else if (priceEu === 0) {
            priceHtml.innerHTML = '<p>Choose options to continue</p>'
        }
    }
}

function addToCart() {
    const notificationSuccess = document.querySelector('.success_fixed')
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

    let data = {
        'action': 'add',
        'productId': productId,
        'optionsId': [],
        'quantity': count.innerText,
    }
    requiredChecked.forEach(input => {
        let option = {
            'optionId': input.closest('.option').getAttribute('data-option-id'),
            'name': input.closest('.option').getAttribute('data-name'),
            'price': input.closest('.option').getAttribute('data-price-'+ currency),
        }
        data['optionsId'].push(option)
    })
    requiredChildChecked.forEach(input => {
        let option = {
            'optionId': input.closest('.option').getAttribute('data-option-id'),
            'name': input.closest('.option').getAttribute('data-name'),
            'price': input.closest('.option').getAttribute('data-price-'+ currency),
        }
        data['optionsId'].push(option)
    })
    additionChecked.forEach(input => {
        let option = {
            'optionId': input.closest('.option').getAttribute('data-option-id'),
            'name': input.closest('.option').getAttribute('data-name'),
            'price': input.closest('.option').getAttribute('data-price-'+ currency),
        }
        data['optionsId'].push(option)
    })
    instance.post('cartService/', data, {
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        product_quantity(response.data.products.length)
    })

    notificationSuccess.style.display = 'block'
    setTimeout(function () {
        notificationSuccess.style.display = 'none'
    }, 2500)
}

const service_info = document.querySelectorAll('.service_item')

service_info.forEach(item => {
    item.addEventListener('mouseover', function () {
        this.querySelector('.service_info').style.display = 'block'
    })
    item.addEventListener('mouseleave', function () {
        this.querySelector('.service_info').style.display = 'none'
    })
})

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

setPrice()
