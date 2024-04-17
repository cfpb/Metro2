import type { ReactElement } from 'react'

import './DefinitionList.less'

export interface Definition {
  term: string
  definition: ReactElement | number | string | null | undefined
}

export interface DefinitionListProperties {
  items: Definition[]
}

export default function DefinitionList({
  items
}: DefinitionListProperties): ReactElement {
  return (
    <dl className='definition-list'>
      {items.map(item => (
        <div key={item.term} className='definition-list__item' data-testid='dl-item'>
          <dt>{item.term}:</dt>
          <dd>{item.definition}</dd>
        </div>
      ))}
    </dl>
  )
}
