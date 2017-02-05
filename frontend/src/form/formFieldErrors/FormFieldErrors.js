import React, { Component, PropTypes } from 'react'

import styles from './formFieldErrors.less'

export default class FormFieldErrors extends Component {
  /*
   * Render errors associated to a field in a list
   */

  render() {
    if (this.props.errors_list && this.props.errors_list[this.props.field]) {
      let errors = this.props.errors_list[this.props.field]
      return (
        <ul className={styles.errorsList}>
          {errors.map(error =>
            <li
              key={error}
            >{error}</li>
          )}
        </ul>
      )
    }
    return null
  }
}
