import { combineReducers } from 'redux'

import user from 'user/reducers'
import modal from 'modal/reducers'

const rootReducer = combineReducers({
  modal,
  user,
})

export default rootReducer
