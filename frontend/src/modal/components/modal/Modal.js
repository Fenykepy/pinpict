import React, { Component, PropTypes } from 'react'


import ModalHeader from '../modalHeader/ModalHeader'

import styles from './modal.less'

export default class Modal extends Component {

  closeModal(e) {
    if (this.props.modal_closable) {
      this.context.closeModal()
    }
  }

  getModalClassNames() {
    let classes = [styles.modal]

    // we add extra classes
    if (this.props.modal_max) { classes.push(styles.max) }
    if (this.props.modal_small) { classes.push(styles.small) }

    return classes.join(" ")
  }

  getOverlayClassNames() {
    let classes = [styles.overlay]

    // we add extra classes
    if (this.props.modal_opaque) { classes.push(styles.opaque) }
    else if (this.props.modal_transparent) {
      classes.push(styles.transparent)
    }

    return classes.join(" ")
  }

  render() {
    
    return (
      <div
        className={this.getOverlayClassNames()}
        onClick={this.closeModal.bind(this)}
      >
        <section
          className={this.getModalClassNames()}
          onClick={e => e.stopPropagation()}
        >
          <ModalHeader
            title={this.props.title}
            closable={this.props.modal_closable}
            closeModal={this.closeModal.bind(this)}
          />
          {this.props.children}
        </section>
      </div>
    )
  }
}

Modal.propTypes = {
  modal_closable: PropTypes.bool,
  modal_max: PropTypes.bool,
  modal_small: PropTypes.bool,
  modal_opaque: PropTypes.bool,
  modal_transparent: PropTypes.bool,
}

Modal.contextTypes = {
  closeModal: PropTypes.func.isRequired,
}
