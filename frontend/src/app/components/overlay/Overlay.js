import React, { Component, PropTypes } from 'react'

import styles from './overlay.less'

export default class Overlay extends Component {

  close() {
    if (this.props.close) {
      this.props.close()
    }
  }

  getClassNames() {
    if (this.props.transparent) return styles.transparent
    if (this.props.opaque) return styles.opaque
    return styles.overlay
  }

  render() {

    return (
      <div
        onClick={this.close.bind(this)}
        className={this.getClassNames()}
      >
        {this.props.children}
      </div>
    )
  }
}

Overlay.propTypes = {
  close: PropTypes.func,
  transparent: PropTypes.bool,
  opaque: PropTypes.bool,
}
