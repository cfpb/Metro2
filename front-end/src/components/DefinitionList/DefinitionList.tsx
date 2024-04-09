import type { ReactElement } from 'react'

import './DefinitionList.less'

interface DefinitionListProperties {
  items: {
    term: string
    definition: ReactElement | number | string
  }[]
}

export default function DefinitionList({
  items
}: DefinitionListProperties): ReactElement {
  return (
    <dl className='definition-list'>
      {items.map(item => (
        <div
          key={item.term}
          className='definition-list__item'
          data-testid='dl-item'>
          <dt>{item.term}</dt>
          <dd>{item.definition}</dd>
        </div>
      ))}
    </dl>
  )
}
