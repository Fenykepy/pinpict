
function getCookieExp(daydelta) {
  /* return cookie formated expiration date,
   * with one day more than current seven by default
   */

  // get current timestamp + day delta (* 1000 because date.now return milliseconds)
  let t = Date.now() + daydelta * 24 * 60 * 60 * 1000
  // return formated date
  return new Date(t).toUTCString()
}

export function getCookie(name) {
  let cname = name + "="
  let cookies = document.cookie.split(';')
  for (let i=0, l=cookies.length; i < l; i++) {
    let cookie = cookies[i].trim()
    if (cookie.substring(0, cname.length) == cname) {
      return cookie.split('=')[1]
    }
  }
  return false
}

export function setCookie(name, value, daydelta = 1) {
  // if no expiration date, set 24h
  let expire = getCookieExp(daydelta)
  document.cookie=`${name}=${value}; expires=${expire}; path=/`
}

export function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`
}
