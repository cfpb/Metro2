import { Icon } from '@cfpb/design-system-react'
import { JSX } from 'react'
import './Loader.scss'

interface Properties {
  message?: string
  hasBackground?: boolean
  className?: string
}

export default function Loader({
  message = 'This page is loading.',
  hasBackground = true,
  className = ''
}: Properties): JSX.Element {
  const loaderClass = ['loader', className]
  if (hasBackground) loaderClass.push('loader--background')
  return (
    <div className={loaderClass.join(' ')} data-testid='loader'>
      <div className='loader__container'>
        <div className='loader__message'>
          <Icon name='updating' size='32px' />
          <span className='loader__text'>{message}</span>
        </div>
      </div>
    </div>
  )
}
