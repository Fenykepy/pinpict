import React, { Component, PropTypes } from 'react'

import Link from 'react-router/lib/Link'

import AccessibilityText from 'app/components/accessibilityText/AccessibilityText'
import HeaderLinks from '../headerLinks/HeaderLinks'

import styles from './header.less'

export default class Header extends Component {

  render() {
    return (
      <header
        role="banner"
        className={styles.header}
      >
        <h1
          className={styles.title}
        >
          <Link
            to={"/"}
            className={styles.link}
          ><AccessibilityText
              text="Pinpict"
          /></Link>
        </h1>
        <HeaderLinks
          authenticated={this.props.authenticated}
        />
      </header>
    )
  }
}


Header.propTypes = {
  authenticated: PropTypes.bool.isRequired,
}
