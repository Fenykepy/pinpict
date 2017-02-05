import React, { Component, PropTypes } from 'react'

// import favicon here, for it to be compiled
import favicon from './favicon.png'

import { connect } from 'react-redux'

import { appSelector } from 'app/selectors'


import Header from '../../components/header/Header'

import {
  closeModal,
  setModal,
} from 'modal/actions'


import styles from './app.less'

class App extends Component {

  getChildContext() {
    // we set setModal and closeModal as context
    // to avoid passing it everywhere
    return {
      setModal: this.setModal.bind(this),
      closeModal: this.closeModal.bind(this),
    }
  }

  setModal(modal) {
    this.props.dispatch(setModal(modal))
  }

  closeModal() {
    this.props.dispatch(closeModal())
  }

  render () {
    // injected by connect call
    const {
      dispatch,
      user,
    } = this.props

    console.log('App', this.props)

    return (
      <div>
        <Header
          authenticated={this.props.user.is_authenticated || false}
        />
        <section
          role="main"
          className={styles.main}
        >
          {this.props.children}
        </section>
      </div>
    )
  }
}

App.childContextTypes = {
  setModal: PropTypes.func.isRequired,
  closeModal: PropTypes.func.isRequired,
}

App.propTypes = {
  dispatch: PropTypes.func.isRequired,
  user: PropTypes.shape({
    is_authenticated: PropTypes.bool,
  }).isRequired
}

// Wrap the component to inject state into it
export default connect(appSelector)(App)
