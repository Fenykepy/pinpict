import React, { Component, PropTypes } from 'react'

import styles from './modalContent.less'

export default class ModalContent extends Component {

  render() {

    return (
      <div
        className={styles.modalContent}
      >
        {this.props.children}
      </div>
    )
  }
}
