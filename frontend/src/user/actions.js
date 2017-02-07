import * as types from './actionsTypes'

import Fetch from 'http'

import { setCookie, getCookie, deleteCookie } from 'cookies'
import { getJWTDate } from 'utils'


// actions creators

// Fetching user
function requestUser() {
  return {
    type: types.USER_REQUEST_USER
  }
}

function requestUserSuccess(user) {
  return {
    type: types.USER_REQUEST_USER_SUCCESS,
    user
  }
}

function requestUserFailure(errors) {
  return {
    type: types.USER_REQUEST_USER_FAILURE,
    errors
  }
}

function shouldFetchUser(state) {
  let user = state.user
  if (! user) return true
  if (user.is_authenticated || user.is_fetching ||
    user.is_logging_in || user.is_registering) return false
  return true
}

export function fetchUserIfNeeded() {
  // fetch user if it's not done yet
  return (dispatch, getState) => {
    if (shouldFetchUser(getState())) {
      return dispatch(fetchUser())
    }
    // else return a resolved promise
    return new Promise((resolve, reject) =>
      resolve({user: getState().user}))
  }
}

function fetchUser() {
  // fetch current user data
  return function(dispatch, getState) {
    // start request
    dispatch(requestUser())
    // return a promise
    return Fetch.get('api/users/current/', getState())
      .then(json =>
        dispatch(requestUserSuccess(json))
      )
      .catch(error => {
        // store error in state
        dispatch(requestUserFailure(error))
        throw error
      })
  }
}


// Logging in
function requestLogin() {
  return {
    type: types.USER_REQUEST_LOGIN
  }
}

function requestLoginSuccess(token) {
  return {
    type: types.USER_REQUEST_LOGIN_SUCCESS,
    token
  }
}

function requestLoginFailure(errors) {
  return {
    type: types.USER_REQUEST_LOGIN_FAILURE,
    errors
  }
}

export function login(credentials) {
  /*
   * try to get token with given credentials
   */
  return function(dispatch, getState) {
    // start request
    dispatch(requestLogin())

    // return a promise
    return Fetch.post('api/token-auth/',
      getState(),
      {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      JSON.stringify(credentials)
    )
    .then(json => {
      // keep cookie with token for 7 days
      setCookie('auth_token', json.token, 7)
      dispatch(requestLoginSuccess(json.token))
    })
    .then(() => {
      // fetch authenticated user's data
      dispatch(fetchUserIfNeeded())
    })
    .catch(error => {
      error.response.json().then(json => {
        // store error in state
        dispatch(requestLoginFailure(json))
      })
    })
  }
}



// Logout
export function logout() {
  // we delete auth cookie
  deleteCookie('auth_token')
  return {
    type: types.USER_LOGOUT
  }
}



// Verify token
function storeToken(token) {
  return {
    type: types.USER_STORE_TOKEN,
    token
  }
}

function requestVerifyToken() {
  return {
    type: types.USER_REQUEST_VERIFY_TOKEN
  }
}

function receivedVerifiedToken(token) {
  return {
    type: types.USER_REQUEST_VERIFY_TOKEN_SUCCESS,
    token
  }
}

function requestVerifyTokenFailure(error) {
  return {
    type: types.USER_REQUEST_VERIFY_TOKEN_FAILURE,
    error
  }
}


export function verifyToken() {
  /*
   * verify if given token is valid
   */
  return function(dispatch, getState) {
    let token = getCookie('auth_token')
    if (token) {
      // store token in state
      dispatch(storeToken(token))
      // start request
      dispatch(requestVerifyToken())
      // return a promise
      return Fetch.post('api/token-verify/',
        getState(),
          {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          JSON.stringify({'token': token})
        )
        .then(json => {
          dispatch(refreshTokenIfNeeded(json.token))
          return dispatch(receivedVerifiedToken(json.token))
        })
        .then(() =>
          // fetch authenticated user's data
          dispatch(fetchUserIfNeeded())
        )
        .catch(error => {
          console.warn(error)
          dispatch(requestVerifyTokenFailure(error))
        })
    }
  }
}


// Refresh token

function requestRefreshToken() {
  return {
    type: types.USER_REQUEST_REFRESH_TOKEN
  }
}

function receivedRefreshToken(token) {
  return {
    type: types.USER_REQUEST_REFRESH_TOKEN_SUCCESS,
    token
  }
}

function requestRefreshTokenFailure(error) {
  return {
    type: types.USER_REQUEST_REFRESH_TOKEN_FAILURE,
    error
  }
}

export function refreshTokenIfNeeded(token) {
  /*
   * refresh token if it expires in less than one day
   */
  return function(dispatch) {
    //console.log('refresh token if needed')
    // we pass expiration date in milliseconds
    let exp = getJWTDate(token) * 1000
    //let delta = 24 * 60 * 60 * 1000
    let delta = 24 * 60 * 60 * 50 * 1000

    if (exp < Date.now() + delta) {
      // token need to be refreshed
      dispatch(refreshToken(token))
    }
  }
}

function refreshToken(token) {
  /*
   * refresh token
   */
  return function(dispatch, getState) {
    //console.log('refresh token')
    // start request
    dispatch(requestRefreshToken())
    // return a promise
    return Fetch.post('api/token-refresh/',
          getState(),
          {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          JSON.stringify({'token': token})
        )
        .then(json => {
          //console.log('refresh token success')
          setCookie('auth_token', json.token, 7)
          return dispatch(receivedRefreshToken(json.token))
        })
        .then(() =>
          // fetch authenticated user's data
          dispatch(fetchUserIfNeeded())
        )
        .catch(error => {
          console.warn(error)
          // check if token is valid
          dispatch(verifyToken())
          dispatch(requestRefreshTokenFailure(error))
        })
  }
}
