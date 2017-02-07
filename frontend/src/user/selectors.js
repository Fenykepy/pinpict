import { createStructuredSelector } from 'reselect'

export const userSelector = state => state.user

export const userDataSelector = state => state.user.user_data
export const authenticatedSelector = state => state.user.is_authenticated

export const loginSelector = createStructuredSelector({
  user: userSelector,
})

export const userMenuSelector = createStructuredSelector({
  user: userDataSelector
})

