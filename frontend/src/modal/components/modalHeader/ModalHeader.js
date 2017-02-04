import React, { Component, PropTypes } from 'react'

import styles from './modalHeader.less'

export default class ModalHeader extends Component {

  getCloseButton() {
    if (this.props.closable) {
      return (
        <button
          className= {styles.closeButton}
          onClick={this.props.closeModal}
        >×</button>
      )
    }
    return null
  }


  render() {

    return (
      <header
        className={styles.modalHeader}
      >
        <h1>{this.props.title}</h1>
        {this.getCloseButton()}
      </header>
    )
  }
}
