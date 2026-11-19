import { Icon } from '@cfpb/design-system-react'
import { JSX } from 'react'
import './Loader.scss'

interface Properties {
  message?: string
  hasBackground?: boolean
  isOverlay?: boolean
  className?: string
  children?: JSX.Element | string
}

export default function Loader({
  message = 'This page is loading.',
  hasBackground = true,
  isOverlay = true,
  className = '',
  children
}: Properties): JSX.Element {
  const loaderClass = ['loader', className]
  if (hasBackground) loaderClass.push('loader--background')
  if (isOverlay) loaderClass.push('loader--overlay')

  return (
    <div className={loaderClass.join(' ')} data-testid='loader'>
      <div className='loader__container'>
        <div className='loader__contents'>
          <div className='loader__message'>
            <Icon name='updating' size='32px' />
            <span className='loader__text'>{message}</span>
          </div>
          {children}
        </div>
      </div>
    </div>
  )
}
