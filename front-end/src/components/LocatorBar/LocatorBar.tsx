import { Breadcrumb, Icon } from '@cfpb/design-system-react'
import type { ReactElement } from 'react'

import './LocatorBar.scss'

interface BreadcrumbCrumb {
  to: string
  label: string
  isCurrent?: boolean
}

/**
 * LocatorBar
 *
 * Implements a full-width header bar with an icon and heading,
 * as well as optional eyebrow, subhead, and breadcrumbs.
 *
 * @param {string} heading - H2-level heading text
 * @param {string} icon - name for a design-system icon
 *                        eg, 'bank' or 'bank-round'
 *                        Full list here:
 *                        https://cfpb.github.io/design-system/foundation/iconography
 * @param {string} eyebrow - text for small heading above the H2
 * @param {string} subhead - text for H3 heading below the H2
 * @param {array} breadcrumbs - array of breadcrumb links
 *                              with format:
 *                              [to:'link url', label:'link text']
 *
 */

interface LocatorBarProperties {
  icon?: string
  heading: string
  eyebrow?: string
  subhead?: string
  breadcrumbs?: BreadcrumbCrumb[] | null
}

export default function LocatorBar({
  heading,
  icon,
  eyebrow,
  subhead,
  breadcrumbs = null
}: LocatorBarProperties): ReactElement {
  let className = 'locator-bar'
  if (breadcrumbs) className += ' locator-bar--actions'

  return (
    <div className={className}>
      {breadcrumbs ? (
        <Breadcrumb crumbs={breadcrumbs} data-testid='locator-bar-breadcrumbs' />
      ) : null}
      <div className='header-with-icon'>
        {icon ? (
          <Icon
            name={icon}
            size='47px'
            data-testid='locator-bar-icon'
            isPresentational
          />
        ) : null}

        <div>
          {eyebrow ? (
            <div className='h5 eyebrow' data-testid='locator-bar-eyebrow'>
              {eyebrow}
            </div>
          ) : null}
          <h1 className='h2' data-testid='locator-bar-heading'>
            {heading}
          </h1>
          {subhead ? (
            <h2 className='h3' data-testid='locator-bar-subhead'>
              {subhead}
            </h2>
          ) : null}
        </div>
      </div>
    </div>
  )
}
