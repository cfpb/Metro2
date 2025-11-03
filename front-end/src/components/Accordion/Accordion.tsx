import type { ReactElement, ReactNode } from 'react'
import { useState } from 'react'

import { Icon } from 'design-system-react'
import './Accordion.scss'

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
  isPadded = false,
  hasBorder = true,
  hasBackground = true,
  ...properties
}: AccordionProperties): ReactElement {
  const [isExpanded, setIsExpanded] = useState(openOnLoad)

  const expandableClasses = ['o-expandable', className]
  if (isExpanded) expandableClasses.push('o-expandable--open')
  if (isPadded) expandableClasses.push('o-expandable--padded')
  if (hasBorder) expandableClasses.push('o-expandable--border')
  if (hasBackground) expandableClasses.push('o-expandable--background')

  const onClick = (): void => {
    setIsExpanded(!isExpanded)
  }

  const expandableLink = (
    <span className='o-expandable__link'>
      <span
        className={`o-expandable__cue o-expandable__cue--${
          isExpanded ? 'close' : 'open'
        }`}>
        <span className='o-expandable__cue-text'>
          <Icon name={isExpanded ? 'up' : 'down'} alt={isExpanded ? 'up' : 'down'} />
        </span>
      </span>
    </span>
  )

  return (
    <div
      className={expandableClasses.join(' ')}
      data-testid='accordion'
      {...properties}>
      {typeof header === 'string' ? (
        <button
          type='button'
          className='o-expandable__header o-expandable__target'
          aria-expanded={isExpanded}
          title={header}
          onClick={onClick}>
          <h3 className='h4 o-expandable__label'>{header}</h3>
          {expandableLink}
        </button>
      ) : (
        <div
          className='o-expandable__header o-expandable__header-interactive'
          aria-expanded={isExpanded}>
          {header}
          <button type='button' className='o-expandable__target' onClick={onClick}>
            {expandableLink}
          </button>
        </div>
      )}

      <div data-testid='accordion-wrapper' className='o-expandable__wrapper'>
        <div data-testid='accordion-inner' className='o-expandable__inner'>
          <div data-testid='accordion-content' className='o-expandable__content'>
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}
