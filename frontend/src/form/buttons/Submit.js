import React, { Component, PropTypes } from 'react'

import styles from './button.less'

export default class Submit extends Component {

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
      <input
        className={this.getClassNames()}
        type="submit"
        value={this.props.value}
        form={this.props.form}
      />
    )
  }
}

Submit.propTypes = {
  className: PropTypes.string,
  value: PropTypes.string.isRequired,
  form: PropTypes.string,
  primary: PropTypes.bool,
  reversed: PropTypes.bool,
  secondary: PropTypes.bool,
  big: PropTypes.bool,
  max: PropTypes.bool,
}
