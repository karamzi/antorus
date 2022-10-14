const button = document.querySelector('#submit_button')
button.addEventListener('click', createOrder)

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
            window.location.replace(data.url)
        }
        button.removeAttribute('disabled')
    })
}

function checkForm(connection, email) {
    connection.classList.remove('input_error')
    email.classList.remove('input_error')
    if (!checkInput(connection)) return false
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
