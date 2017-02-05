import React, { Component, PropTypes } from 'react'

import spinner_svg from './spinner.svg'
import styles from './spinner.less'
/*
 * using a svg spinner optimized with svgo rotating with css3
 * we pass from 8kb to 4kb
 */
export default class Spinner extends Component {
  render() {

    return (
      <div className={styles.spinner}>
          <img src={spinner_svg} alt="spinner" height="40px"/>
        <p><em>{this.props.message}</em></p>
      </div>
    )
  }
}

Spinner.propTypes = {
  message: PropTypes.string,
}
