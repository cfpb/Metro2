import type { ReactElement } from 'react'
import Breadcrumbs from './Breadcrumbs'
import './Breadcrumbs.less'
import './LocatorBar.less'

interface LocatorBarProperties {
  heading: string
  eyebrow?: string
  subhead?: string
  breadcrumbs?: boolean
}

export default function LocatorBar({
  heading,
  eyebrow,
  subhead,
  breadcrumbs = false
}: LocatorBarProperties): ReactElement {
  let className = 'locator-bar'
  if (breadcrumbs) className += ' locator-bar__actions'

  return (
    <div className={className}>
      {breadcrumbs ? <Breadcrumbs /> : null}
      {eyebrow ? (
        <h4 className='h5 eyebrow' data-testid='eyebrow'>
          {eyebrow}
        </h4>
      ) : null}
      <h2 data-testid='heading'>{heading}</h2>
      {subhead ? <h3 data-testid='subhead'>{subhead}</h3> : null}
    </div>
  )
}
