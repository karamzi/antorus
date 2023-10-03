const button = document.querySelector('#submit_button')
const paymentOptions = document.querySelectorAll('.payment_option')
const paymentMessages = document.querySelector('.payment_information').querySelectorAll('.success')
let chosenPaymentType = null

button.addEventListener('click', createOrder)

paymentOptions.forEach(item => {
    item.addEventListener('click', choosePaymentType)
})

function createOrder() {
    const connection = document.getElementById('connection')
    const email = document.getElementById('email')
    const comment = document.getElementById('comment').value
    if (!checkForm(connection, email)) {
        return
    }
    let data = new FormData()
    data.append('currency', currency)
    data.append('connection', connection.value)
    data.append('email', email.value)
    data.append('comment', comment)
    data.append('payment_type', chosenPaymentType)
    button.setAttribute('disabled', 'disabled')
    instance.post('createOrder/', data, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => {
        if (response.status === 200) {
            data = response.data
            ym(67968427,'reachGoal','order')
            switch (chosenPaymentType) {
                case 'plisio':
                    window.location.replace(data.url)
                    break
                case 'stripe':
                    paymentForm(data.order_number, '/stripe/', 'stripe')
                    break
                case 'paypal':
                    paymentForm(data.order_number, '/paypal/', 'paypal')
                    break
                default:
                    console.log('error')
            }
        } else if (response.status === 500) {
            console.log('Error 500')
        }
        button.removeAttribute('disabled')
    })
}

function checkForm(connection, email) {
    connection.classList.remove('input_error')
    email.classList.remove('input_error')
    if (!checkInput(connection)) return false
    if (!checkEmail(email)) return false
    if (!checkPaymentType()) return false
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
    return true
}

function checkEmail(email) {
    const pattern = /^[a-zA-Z0-9][\-_\.\+\!\#\$\%\&\'\*\/\=\?\^\`\{\|]{0,1}([a-zA-Z0-9][\-_\.\+\!\#\$\%\&\'\*\/\=\?\^\`\{\|]{0,1})*[a-zA-Z0-9]@[a-zA-Z0-9][-\.]{0,1}([a-zA-Z][-\.]{0,1})*[a-zA-Z0-9]\.[a-zA-Z0-9]{1,}([\.\-]{0,1}[a-zA-Z]){0,}[a-zA-Z0-9]{0,}$/i
    if (pattern.test(email.value)){
       return true
    }
    email.classList.add('input_error')
    return false
}

function checkPaymentType() {
    if (chosenPaymentType === null) {
        const errorDiv = document.querySelector('.error')
        errorDiv.style.display = 'block'
        setTimeout(() => {
            errorDiv.style.display = 'none'
        }, 2000)
        return false
    }
    return true
}

function choosePaymentType() {
    const index = this.getAttribute('data-index')

    paymentOptions.forEach(item => {
        item.classList.remove('payment_option_active')
    })

    paymentMessages.forEach(item => {
        item.style.display = 'none'
    })

    this.classList.add('payment_option_active')
    chosenPaymentType = this.getAttribute('data-payment-type')

    paymentMessages[index].style.display = 'block'
}

function paymentForm(orderNumber, location, paymentType) {
    const form = document.createElement('form')
    const orderNumberInput = document.createElement('input')
    const paymentTypeInput = document.createElement('input')
    const csrfMiddleWareTokenInput = document.createElement('input')

    form.style.display = 'none'
    form.method = 'POST'
    form.action = location

    csrfMiddleWareTokenInput.name = 'csrfmiddlewaretoken'
    csrfMiddleWareTokenInput.value = getCookie('csrftoken')

    orderNumberInput.name  = 'order_number'
    orderNumberInput.value = orderNumber

    paymentTypeInput.name = 'payment_type'
    paymentTypeInput.value = paymentType

    form.appendChild(csrfMiddleWareTokenInput)
    form.appendChild(orderNumberInput)
    form.appendChild(paymentTypeInput)
    document.body.appendChild(form)
    form.submit()
}
