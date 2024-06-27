import LocatorBar from 'components/LocatorBar/LocatorBar'
import type { ReactElement } from 'react'
import './GuidePage.less'

export default function GuidePage(): ReactElement {

  return (
    <>
      <LocatorBar
        eyebrow={`Metro2 User Guide`}
        heading='Metro 2 Need to Know(s)'
        icon='book'
      />
      <div className='content-row'>
        <p>Silly Billy! Trix are for kids.</p>
      </div>
    </>
  )
}
