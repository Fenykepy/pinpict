import React, { Component, PropTypes } from 'react'

import styles from './formWrapper.less'

export default class FormWrapper extends Component {

  render() {
    return (
      <article
        className={styles.formWrapper}
      >
        {this.props.children}
      </article>
    )
  }
}



