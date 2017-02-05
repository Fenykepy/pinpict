import * as types from './actionsTypes'

import Fetch from 'http'

import { setCookie, getCookie, deleteCookie } from 'cookies'
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
      resolve({user: getState().user.user}))
  }
}

function fetchUser() {
  // fetch current user data
  return function(dispatch) {
    // start request
    dispatch(requestUser())
    // return a promise
    return Fetch.get('api/users/current/')
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
      dispatch(fetchCurrentUserIfNeeded())
    })
    .catch(error => {
      error.response.json().then(json => {
        // store error in state
        dispatch(requestLoginFailure(json))
      })
    })
  }
}





