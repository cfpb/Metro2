import type { ReactElement, ReactNode } from 'react'
import { useState } from 'react'

import { Icon } from 'design-system-react'
import './Accordion.less'

export interface AccordionProperties {
  header: ReactNode
  children: ReactNode
  className?: string
  // inAccordionGroup?: boolean
  openOnLoad?: boolean
  isPadded?: boolean
  hasBorder?: boolean
  hasBackground?: boolean
}

export default function Accordion({
  header,
  children,
  // inAccordionGroup = false,
  openOnLoad = false,
  className = '',
  isPadded = true,
  hasBorder = true,
  hasBackground = true,
  ...properties
}: AccordionProperties): ReactElement {
  const [isExpanded, setIsExpanded] = useState(openOnLoad)

  const expandableClasses = ['o-expandable', className]
  if (isExpanded) expandableClasses.push('o-expandable__open')
  if (isPadded) expandableClasses.push('o-expandable__padded')
  if (hasBorder) expandableClasses.push('o-expandable__border')
  if (hasBackground) expandableClasses.push('o-expandable__background')

  const onClick = (): void => {
    setIsExpanded(!isExpanded)
  }

  const expandableLink = (
    <span className='o-expandable_link'>
      <span
        className={`o-expandable_cue o-expandable_cue__${
          isExpanded ? 'close' : 'open'
        }`}>
        <span className='o-expandable_cue-text'>
          <Icon name={isExpanded ? 'up' : 'down'} alt={isExpanded ? 'up' : 'down'} />
        </span>
      </span>
    </span>
  )

  return (
    <div
      className={expandableClasses.join(' ')}
      data-test-id='accordion'
      {...properties}>
      {typeof header === 'string' ? (
        <button
          type='button'
          className='o-expandable_header o-expandable_target'
          aria-expanded={isExpanded}
          title={header}
          onClick={onClick}>
          <h3 className='h4 o-expandable_label'>{header}</h3>
          {expandableLink}
        </button>
      ) : (
        <div
          className='o-expandable_header o-expandable_header-interactive'
          aria-expanded={isExpanded}>
          {header}
          <button type='button' className='o-expandable_target' onClick={onClick}>
            {expandableLink}
          </button>
        </div>
      )}
      <div className='o-expandable_content'>
        <div className='o-expandable_inner'>{children}</div>
      </div>
    </div>
  )
}
