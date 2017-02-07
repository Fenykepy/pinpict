import React, { Component, PropTypes } from 'react'

import styles from './dropdownList.less'

export default class DropdownList extends Component {

  render() {

    return (
      <ul
        className={styles.list}
      >
        {this.props.children}
      </ul>
    )
  }
}
