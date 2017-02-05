import {
  USER_REQUEST_LOGIN,
  USER_REQUEST_LOGIN_SUCCESS,
  USER_REQUEST_LOGIN_FAILURE,
  USER_REQUEST_REGISTER,
  USER_REQUEST_REGISTER_SUCCESS,
  USER_REQUEST_REGISTER_FAILURE,
  USER_REQUEST_USER,
  USER_REQUEST_USER_SUCCESS,
  USER_REQUEST_USER_FAILURE,
  USER_REQUEST_VERIFY_TOKEN,
  USER_REQUEST_VERIFY_TOKEN_SUCCESS,
  USER_REQUEST_VERIFY_TOKEN_FAILURE,
  USER_LOGOUT,
  USER_STORE_TOKEN,
} from './actionsTypes'

function user(state = {}, action) {
  switch (action.type) {
    case USER_STORE_TOKEN:
      return Object.assign({}, state, {
        token: action.token,
      })
    case USER_REQUEST_USER:
      return Object.assign({}, state, {
        user_is_fetching: true,
        user_fetched: false,
      })
    case USER_REQUEST_USER_SUCCESS:
      return Object.assign({}, state, {
        user_is_fetching: false,
        user_fetched: true,
        user_data: action.user,
      })
    case USER_REQUEST_USER_FAILURE:
      return Object.assign({}, state, {
        user_is_fetching: false,
        user_fetched: false,
        user_errors: action.errors,
      })
    case USER_REQUEST_LOGIN:
      return Object.assign({}, state, {
        is_authenticated: false,
        is_logging_in: true,
        token: null,
      })
    case USER_REQUEST_LOGIN_SUCCESS:
      return Object.assign({}, state, {
        is_authenticated: true,
        is_logging_in: false,
        token: action.token,
      })
    case USER_REQUEST_LOGIN_FAILURE:
      return Object.assign({}, state, {
        is_authenticated: false,
        is_logging_in: false,
        token: null,
        login_errors: action.errors,
      })
    case USER_REQUEST_VERIFY_TOKEN:
      return Object.assign({}, state, {
        is_verifying_token: true,
      })
    case USER_REQUEST_VERIFY_TOKEN_SUCCESS:
      return Object.assign({}, state, {
        is_verifying_token: false,
        is_authenticated: true,
      })
    case USER_REQUEST_VERIFY_TOKEN_FAILURE:
      return Object.assign({}, state, {
        is_verifying_token: false,
        is_authenticated: false,
        token_errors: action.errors,
      })
    case USER_REQUEST_REGISTER:
      return {
        is_authenticated: false,
        is_registering: true,
      }
    case USER_REQUEST_REGISTER_SUCCESS:
      return {
        is_authenticated: true,
        is_registering: false,
        token: action.token,
      }
    case USER_REQUEST_REGISTER_FAILURE:
      return {
        is_authenticated: false,
        is_registering: false,
        register_errors: action.errors,
      }
    case USER_LOGOUT:
      return {}
    default:
      return state
  }
}

export default user
