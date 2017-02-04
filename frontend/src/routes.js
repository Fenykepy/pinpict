import React from 'react'
import { render } from 'react-dom'

import Route from 'react-router/lib/Route'

import App from 'app/containers/app/App'

export default ()=> {
  return (
    <Route>
      <Route path="/" component={App}>
      </Route>
    </Route>
  )
}
