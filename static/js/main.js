const usButton = document.getElementById('us')
const euButton = document.getElementById('eu')

usButton.addEventListener('click', () => {
    setCookie('us', 'currency')
    window.location.reload()
})
euButton.addEventListener('click', () => {
    setCookie('eu', 'currency')
    window.location.reload()
})


function getCookie(name) {
    let results = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)')

    if (results)
        return JSON.parse(unescape(results[2]))
    else
        return []
}


function setCookie(value, name) {
    let expires = ""
    let date = new Date()
    date.setTime(date.getTime() + (90 * 1000))
    expires = "; expires=" + date.toUTCString()
    document.cookie = name + "=" + (value || "") + expires + ";" + ' path=/;'
}