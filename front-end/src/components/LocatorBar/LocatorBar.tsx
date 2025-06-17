import { Icon } from 'design-system-react'
import type { ReactElement } from 'react'
import type { Breadcrumb } from './Breadcrumbs'

import { Breadcrumbs } from './Breadcrumbs'
import './Breadcrumbs.less'
import './LocatorBar.less'

/**
 * LocatorBar
 *
 * Implements a full-width header bar with an icon and heading,
 * as well as optional eyebrow, subhead, and breadcrumbs.
 *
 * @param {string} heading - H2-level heading text
 * @param {string} icon - name for a design-system icon
 *                        eg, 'bank' or 'bank-round'
 * @param {string} eyebrow - text for small heading above the H2
 * @param {string} subhead - text for H3 heading below the H2
 * @param {array} breadcrumbs - array of breadcrumb links
 *                              with format:
 *                              [href:'link url', text:'link text']
 *
 */

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
      {breadcrumbs ? (
        <Breadcrumbs links={breadcrumbs} data-testid='locator-bar-breadcrumbs' />
      ) : null}
      <div className='header-with-icon'>
        <Icon name={icon} size='47px' data-testid='locator-bar-icon' />
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
