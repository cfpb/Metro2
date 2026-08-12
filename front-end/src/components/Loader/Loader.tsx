import { Icon } from '@cfpb/design-system-react'
import { JSX } from 'react'
import './Loader.scss'

interface Properties {
  message?: string
  hasBackground?: boolean
}

export default function Loader({
  message = 'This page is loading.',
  hasBackground = true
}: Properties): JSX.Element {
  return (
    <div
      className={`loader ${hasBackground ? 'loader--background' : ''}`}
      data-testid='loader'>
      <div className='loader__container'>
        <div className='loader__message'>
          <Icon name='updating' size='32px' />
          <span className='loader__text'>{message}</span>
        </div>
      </div>
    </div>
  )
}
