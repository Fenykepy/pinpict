import React, { Component, PropTypes } from 'react'

import { connect } from 'react-redux'

import { userMenuSelector } from 'user/selectors'

import { logout } from 'user/actions'

import UserMenu from 'user/components/userMenu/UserMenu'

import styles from './userMenuButton.less'

class UserMenuButton extends Component {

  constructor(props) {
    super(props)

    this.state = {
      menu: false
    }
  }

  toogleMenu(e) {
    e.preventDefault()
    this.setState({menu: ! this.state.menu})
  }

  closeMenu() {
    this.setState({menu: false})
  }

  logout(e) {
    e.preventDefault()
    this.props.dispatch(logout())
  }

  getMenu() {
    if (this.state.menu) {
      return (
        <UserMenu
          close={this.closeMenu.bind(this)}
          logout={this.logout.bind(this)}
          admin={this.props.user.admin}
        />
      )
    }
    return null
  }

  render() {
    // injected by connect call
    const {
      dispatch,
      user,
    } = this.props

    console.log('UserMenuButton', this.props)

    if (! this.props.user) return null

    return (
      <div
        className={styles.wrapper}
      >
        <button
          className={styles.userMenu}
          onClick={this.toogleMenu.bind(this)}
        ><div>{this.props.user.username}</div>
        </button>
        {this.getMenu()}
      </div>
    )
  }
}

// wrap the component to inject dispatch and state into it
export default connect (userMenuSelector)(UserMenuButton)

UserMenuButton.propTypes = {
  user: PropTypes.shape({
    username: PropTypes.string,
  }),
}
