import { PII_COOKIE_NAME } from '../constants/settings'

/**
 * setCookie
 *
 * Sets a cookie with the given name, value, and expire time (in days).
 * Expire time defaults to 1 day.
 *
 * Linting rule suggests use of cookieStore API (which we avoid due to lack
 * of Safari support) or a cookie library.
 *
 * @param {string} cookieName - name for the cookie
 * @param {boolean | number | string} cookieValue - value for the cookie
 * @param {number} expires - (optional) expire time in days
 *
 */
export const setCookie = (
  cookieName: string,
  cookieValue: boolean | number | string,
  expires = 1
): void => {
  // eslint-disable-next-line unicorn/no-document-cookie
  document.cookie = `${cookieName}=${cookieValue}; max-age=${expires * 86_400}`
}

/**
 * getCookie
 *
 * Given a cookie name, retrieves cookie value
 *
 * Linting rule suggests use of cookieStore API (which we avoid due to lack
 * of Safari support) or a cookie library.
 *
 * @param {string} cookieName - name of the cookie
 * @returns {boolean | number | string} - value of the cookie
 *
 */
export const getCookie = (cookieName: string): string | undefined =>
  // eslint-disable-next-line unicorn/no-document-cookie
  document.cookie
    .split('; ')
    .find(item => item.startsWith(`${cookieName}=`))
    ?.split('=')[1]

/**
 * acceptPIIWarning
 *
 * Sets a cookie with constant PII_COOKIE_NAME
 * to reflect that the PII warning has been acknowledged.
 * Cookie expires in 1 day.
 *
 */
export const acceptPIIWarning = (): void => {
  setCookie(PII_COOKIE_NAME, true)
}

/**
 * hasAcceptedPIIWarning
 *
 * Checks for a cookie indicating PII warning has been acknowledged.
 *
 */
export const hasAcceptedPIIWarning = (): boolean => !!getCookie(PII_COOKIE_NAME)
