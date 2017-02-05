import React, { Component, PropTypes } from 'react'

import Link from 'react-router/lib/Link'

import styles from './button.less'

export default class LinkButton extends Component {

  getClassNames() {
    let classes = []
    
    // we add extra classes
    if (this.props.className) { classes.push(this.props.className) }

    if (this.props.primary) {
      classes.push(styles.primary)
    } else if (this.props.secondary) {
      classes.push(styles.secondary)
    } else if (this.props.reversed) {
      classes.push(styles.reversed)
    } else {
      classes.push(styles.default)
    }

    if (this.props.big) classes.push(styles.big)

    if (this.props.max) classes.push(styles.max)

    return classes.join(" ")
  }

  render() {
    return (
      <Link
        className={this.getClassNames()}
        to={this.props.to}
        onClick={this.props.onClick}
        role="button"
      >{this.props.children}</Link>
    )
  }
}

LinkButton.propTypes = {
  className: PropTypes.string,
  onClick: PropTypes.func,
  big: PropTypes.bool,
  max: PropTypes.bool,
  to: PropTypes.string.isRequired,
}
