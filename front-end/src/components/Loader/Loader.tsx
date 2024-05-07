import { Icon } from 'design-system-react'
import './Loader.less'

interface Properties {
  message?: string
  hasBackground?: boolean
}

export default function Loader({
  message = 'This page is loading.',
  hasBackground = true
}: Properties): JSX.Element {
  return (
    <div className={`loader ${hasBackground ? 'loader__background' : ''}`}>
      <div className='loader_container'>
        <div className='loader_message'>
          <Icon name='updating' size='32px' />
          <span className='loader_text'>{message}</span>
        </div>
      </div>
    </div>
  )
}
