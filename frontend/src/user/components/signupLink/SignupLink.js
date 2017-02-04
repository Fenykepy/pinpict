import React, { Component, PropTypes } from 'react'

import Link from 'react-router/lib/Link'

export default class SignupLink extends Component {
  
  render() {
    return (
      <Link
        className={this.props.className}
        activeClassName={this.props.activeClassName}
        to={'/signup/'}
      >Sign up</Link>
    )
  }
}

SignupLink.propTypes = {
  className: PropTypes.string,
  activeClassName: PropTypes.string,
}
