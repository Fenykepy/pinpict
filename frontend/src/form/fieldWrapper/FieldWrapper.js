import React, { Component, PropTypes } from 'react'

import styles from './fieldWrapper.less'

export default class FieldWrapper extends Component {

  render() {
    return (
      <div
        className={styles.fieldWrapper}
      >
        {this.props.children}
      </div>
    )
  }
}
