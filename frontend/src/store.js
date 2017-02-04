import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'

export const createStoreWithMiddleware = applyMiddleware(
  thunkMiddleware // lets us dispatch() functions
)(createStore)
