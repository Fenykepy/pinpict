import React, { Component, PropTypes } from 'react'

import styles from './modalFooter.less'

export default class ModalFooter extends Component {

  render() {

    return (
      <footer
        className={styles.modalFooter}
      >
        {this.props.children}
      </footer>
    )
  }
}

ModalFooter.propTypes = {
  className: PropTypes.string,
}
