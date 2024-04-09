import type { ReactElement } from 'react'

import './HeaderNavbar.less'
// eslint-disable-next-line import/no-absolute-path
import logo from '/images/logo_237x50@2x.png'

export default function HeaderNavbar(): ReactElement {
  return (
    <header>
      <div className='header-navigation'>
        <div className='o-header_logo'>
          <a href='/'>
            <img
              className='o-header_logo-img'
              src={logo}
              alt='Consumer Financial Protection Bureau'
              width='237'
              height='50'
            />
          </a>
        </div>
      </div>
    </header>
  )
}
