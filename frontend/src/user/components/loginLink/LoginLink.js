import React, { Component, PropTypes } from 'react'

import Link from 'react-router/lib/Link'

export default class LoginLink extends Component {
  
  render() {
    return (
      <Link
        className={this.props.className}
        activeClassName={this.props.activeClassName}
        to={'/login/'}
      >Log in</Link>
    )
  }
}

LoginLink.propTypes = {
  className: PropTypes.string,
  activeClassName: PropTypes.string,
}
