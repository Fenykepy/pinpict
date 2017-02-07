import React, { Component, PropTypes } from 'react'

import Overlay from 'app/components/overlay/Overlay'

import styles from './dropdownMenu.less'

export default class DropdownMenu extends Component {

  render() {
    return (
      <div>
        <Overlay 
          close={this.props.close}
          transparent={true}
        />
        <div
          className={styles.dropdown}
        >
          {this.props.children}
        </div>
      </div>
    )
  }
}

DropdownMenu.propTypes = {
  close: PropTypes.func.isRequired,
  className: PropTypes.string,
}

