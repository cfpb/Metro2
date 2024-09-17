import { Icon } from 'design-system-react'
import type { ReactElement } from 'react'
import type { Breadcrumb } from './Breadcrumbs'

import { Breadcrumbs } from './Breadcrumbs'
import './Breadcrumbs.less'
import './LocatorBar.less'

interface LocatorBarProperties {
  icon: string
  heading: string
  eyebrow?: string
  subhead?: string
  breadcrumbs?: Breadcrumb[] | null
}

export default function LocatorBar({
  heading,
  icon,
  eyebrow,
  subhead,
  breadcrumbs = null
}: LocatorBarProperties): ReactElement {
  let className = 'locator-bar'
  if (breadcrumbs) className += ' locator-bar__actions'

  return (
    <div className={className}>
      {breadcrumbs ? <Breadcrumbs links={breadcrumbs} /> : null}
      <div className='header-with-icon'>
        <Icon name={icon} size='47px' />
        <div>
          {eyebrow ? (
            <div className='h5 eyebrow' data-testid='locator-bar-eyebrow'>
              {eyebrow}
            </div>
          ) : null}
          <h2 data-testid='locator-bar-heading'>{heading}</h2>
          {subhead ? <h3 data-testid='locator-bar-subhead'>{subhead}</h3> : null}
        </div>
      </div>
    </div>
  )
}
