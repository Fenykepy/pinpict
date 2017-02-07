import React, { Component, PropTypes } from 'react'

import DropdownMenu from 'app/components/dropdownMenu/DropdownMenu'
import DropdownList from 'app/components/dropdownList/DropdownList'

export default class UserMenu extends Component {

  render() {
    return (
      <div>
        <DropdownMenu
          close={this.props.close}
        >
          <DropdownList>
            <li><a
                href=""
                onClick={this.props.logout}
            >Logout</a></li>
          </DropdownList>
        </DropdownMenu>
      </div>
    )
  }
}

UserMenu.propTypes = {
  admin: PropTypes.bool,
  logout: PropTypes.func.isRequired,
  close: PropTypes.func.isRequired,
}
