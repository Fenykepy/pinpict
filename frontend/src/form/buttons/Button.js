import React, { Component, PropTypes } from 'react'

import styles from './button.less'

export default class Button extends Component {

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

    if (this.props.shy) classes.push(styles.shy)

    if (this.props.max) classes.push(styles.max)

    return classes.join(" ")
  }

  render() {
    return (
      <button
        className={this.getClassNames()}
        onClick={this.props.onClick}
        type="button"
        title={this.props.title || ""}
      >{this.props.children}</button>
    )
  }
}

Button.propTypes = {
  className: PropTypes.string,
  onClick: PropTypes.func,
  primary: PropTypes.bool,
  reversed: PropTypes.bool,
  secondary: PropTypes.bool,
  big: PropTypes.bool,
  max: PropTypes.bool,
}
