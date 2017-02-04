// import a promise polyfill
require('es6-promise').polyfill()
// import less files
require('styles/controller.less')

import React from 'react'
import { render } from 'react-dom'

import { Provider } from 'react-redux'
import { createStoreWithMiddleware } from 'store'
import rootReducer from 'rootReducer'

import browserHistory from 'react-router/lib/browserHistory'
import Router from 'react-router/lib/Router'

import getRoutes from './routes'


let store = createStoreWithMiddleware(rootReducer)

// every time state changes, log it
/*
let unsusbscribe = store.subscribe(() =>
  console.log('state', store.getState())
)
*/

const routes = <Router

  history={browserHistory}
  routes={getRoutes()}
/>

render(
  <Provider store={store}>
    {routes}
  </Provider>,
  document.getElementById('root')
)
