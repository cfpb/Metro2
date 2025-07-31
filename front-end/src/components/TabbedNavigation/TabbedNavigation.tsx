import { Icon } from 'design-system-react'
import type { ReactElement } from 'react'
import './TabbedNavigation.less'

interface Tab {
  id: number | string
  text: string
  icon: string
  isActive: boolean
}

interface TabbedNavigationProperties {
  tabs: Tab[]
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void
}

export default function TabbedNavigation({
  tabs,
  onClick
}: TabbedNavigationProperties): ReactElement {
  const onTabClick = (event: React.MouseEvent<HTMLButtonElement>): void => {
    onClick?.(event)
  }

  return (
    <div className='tabbed_navigation'>
      <fieldset className='o-form_fieldset'>
        {tabs.map(tab => (
          <button
            type='button'
            onClick={onTabClick}
            className={`tab ${tab.isActive ? 'active' : ''}`}
            key={tab.id}
            id={String(tab.id)}
            data-testid={tab.id}>
            <Icon name={tab.icon} />
            <span className='link-text'>{tab.text}</span>
          </button>
        ))}
      </fieldset>
    </div>
  )
}
