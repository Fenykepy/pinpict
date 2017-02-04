import {
  SET_MODAL,
  CLOSE_MODAL
} from './actionsTypes'

function modal(state=null, action) {
  switch (action.type) {
    case CLOSE_MODAL:
      return null
    case SET_MODAL:
      return action.modal
    default:
      return state
  }
}

export default modal
