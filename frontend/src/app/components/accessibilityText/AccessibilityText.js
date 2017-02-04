import React, { Component, PropTypes } from 'react'

import styles from './accessibilityText.less'

export default class AccessibilityText extends Component {

  render() {
    return (
      <span className={styles.accessibilityText}>
        {this.props.text}
      </span>
    )
  }
}

AccessibilityText.propTypes = {
  text: PropTypes.string.isRequired,
}
