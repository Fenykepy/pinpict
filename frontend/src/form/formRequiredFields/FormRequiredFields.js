import React, { Component, PropTypes } from 'react'

import FormRequiredField from '../formRequiredField/FormRequiredField'
import FieldWrapper from '../fieldWrapper/FieldWrapper'

export default class FormRequiredFields extends Component {

  render() {
    return (
      <FieldWrapper>
        <FormRequiredField /> : required fields.
      </FieldWrapper>
    )
  }
}
