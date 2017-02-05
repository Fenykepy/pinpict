import { createStructuredSelector } from 'reselect'

import {
  userSelector,
  authenticatedSelector,
} from 'user/selectors'

export const appSelector = createStructuredSelector({
  user: userSelector,
})


