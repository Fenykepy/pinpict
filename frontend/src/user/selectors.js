import { createStructuredSelector } from 'reselect'

export const userSelector = state => state.user

export const authenticatedSelector = state => state.user.is_authenticated

export const loginSelector = createStructuredSelector({
  user: userSelector,
})


