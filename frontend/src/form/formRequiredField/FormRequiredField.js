import React, { Component, PropTypes } from 'react'

import styles from './formRequiredField.less'
export default class FormRequiredField extends Component {

  render() {
    return (
      <span className={styles.requiredField}> *</span>
    )
  }
}
