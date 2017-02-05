import React, { Component, PropTypes } from 'react'

import styles from './buttonsWrapper.less'

export default class ButtonsWrapper extends Component {

  render() {
    return (
      <div
        className={styles.buttonsWrapper}
      >
        {this.props.children}
      </div>
    )
  }
}
