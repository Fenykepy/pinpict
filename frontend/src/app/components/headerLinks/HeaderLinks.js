import React, { Component, PropTypes } from 'react'

import LoginLink from 'user/components/loginLink/LoginLink'
import SignupLink from 'user/components/signupLink/SignupLink'

import UserMenuButton from 'user/containers/userMenuButton/UserMenuButton'

import styles from './headerLinks.less'

export default class HeaderLinks extends Component {

  render() {

    if (this.props.authenticated) {
      // we show user menu button
      return (
        <ul className={styles.headerLinks}>
          <li><UserMenuButton /></li>
        </ul>
      )
    }

    return (
      <ul className={styles.headerLinks}>
        <li><LoginLink
            className={styles.link}
            activeClassName={styles.linkActive}
        /></li>
        <li><SignupLink
            className={styles.link}
            activeClassName={styles.linkActive}
        /></li>
      </ul>
    )
  }
}

HeaderLinks.propTypes = {
  authenticated: PropTypes.bool,
}
