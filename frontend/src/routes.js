import React from 'react'
import { render } from 'react-dom'

import Route from 'react-router/lib/Route'

import App from 'app/containers/app/App'
import Login from 'user/containers/login/Login'

export default ()=> {
  return (
    <Route>
      <Route path="/" component={App}>
        <Route path="/login/" component={Login} />
      </Route>
    </Route>
  )
}
