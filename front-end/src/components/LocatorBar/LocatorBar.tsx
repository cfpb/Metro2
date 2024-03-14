import type { ReactElement } from 'react'
import Breadcrumbs from './Breadcrumbs'
import './LocatorBar.less'
import './Breadcrumbs.less'
    
interface LocatorBarProperties {
  heading: string,
  eyebrow?: string,
  subhead?: string,
  breadcrumbs?: boolean
}

export default function LocatorBar( {
  heading,
  eyebrow,
  subhead,
  breadcrumbs = false
}: LocatorBarProperties ): ReactElement {
  let className = 'locator-bar' 
  if ( breadcrumbs ) className += ' locator-bar__actions'

  return (
    <div className={ className }>
      { breadcrumbs ? <Breadcrumbs/> : null }
      { eyebrow 
        ? <h4 className='h5 eyebrow' data-test-id='eyebrow'>{ eyebrow }</h4> 
        : null }
      <h2>{ heading }</h2>
      { subhead ? <h3 data-testid="subhead">{ subhead }</h3> : null }
    </div>
  )
}
