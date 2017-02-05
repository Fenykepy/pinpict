import React, { Component, PropTypes } from 'react'

import { connect } from 'react-redux'

import { loginSelector } from 'user/selectors'

import { login } from 'user/actions'
import { setDocumentTitle } from 'app/actions'

import LoginForm from 'user/components/loginForm/LoginForm'
import SignupLink from 'user/components/signupLink/SignupLink'
import Spinner from 'app/components/spinner/Spinner'
import FormWrapper from 'form/formWrapper/FormWrapper'
import FieldWrapper from 'form/fieldWrapper/FieldWrapper'
import Submit from 'form/buttons/Submit'

const LOGIN_FORM = "login-form"

class Login extends Component {

  constructor(props) {
    super(props)

    this.state = {
      username: '',
      password: '',
    }
  }

  componentWillMount() {
    this.componentWillRender(this.props)
  }

  componentDidMount() {
    // we set title
    setDocumentTitle('Sign in')
  }

  componentWillReceiveProps(nextProps) {
    this.componentWillRender(nextProps)
  }

  componentWillRender(props) {
    // redirect to next url or home if user is authenticated
    if (props.user.is_authenticated) {
      let next = props.location.query.next || '/'
      console.log(`user authenticated, redirect to ${next}`)
      this.context.router.push(next)
    }
  }


  handleUsernameChange(e) {
    this.setState({username: e.target.value})
  }

  handlePasswordChange(e) {
    this.setState({password: e.target.value})
  }

  handleLogin(e) {
    e.preventDefault()
    this.props.dispatch(login(this.state))
  }

  render() {
    // injected by connect call
    const {
      dispatch,
      user
    } = this.props

    console.log('Login', this.props)

    // show spinner if user is logging in
    if (this.props.user.is_logging_in) {
      return (<Spinner message="Logging in..." />)
    }

    return (
      <FormWrapper>
        <h1>Log In to PinPict</h1>
        <LoginForm
          id={LOGIN_FORM}
          onSubmit={this.handleLogin.bind(this)}
          handleUsernameChange={this.handleUsernameChange.bind(this)}
          handlePasswordChange={this.handlePasswordChange.bind(this)}
          username={this.state.username}
          password={this.state.password}
          errors={this.props.user.login_errors}
        />
        <footer>
          <FieldWrapper>
            <Submit
              primary={true}
              max={true}
              form={LOGIN_FORM}
              value="Log in"
            />
          </FieldWrapper>
          <div>No account yet? <SignupLink /></div>
        </footer>
      </FormWrapper>
    )
  }
}

Login.contextTypes = {
  router: React.PropTypes.object.isRequired,
}

// Wrap the component to inject dispatch and state into it
export default connect(loginSelector)(Login)
