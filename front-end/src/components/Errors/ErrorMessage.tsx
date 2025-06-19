import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import './ErrorMessage.less'

interface ErrorMessageProperties {
  title: string
  description: string
}

export default function ErrorMessage({
  title,
  description
}: ErrorMessageProperties): ReactElement {
  return (
    <div className='error-container content-row' data-testid='error-container'>
      <div data-testid='error-message' className='error-message'>
        <h2 data-testid='error-title' className='h1'>
          {title}
        </h2>
        <p data-testid='error-description'>{description}</p>
        <div className='m-btn-group'>
          <Link to='/' className='a-btn a-btn__full-on-xs' data-testid='back-button'>
            Back to Metro 2 home page
          </Link>
        </div>
      </div>
    </div>
  )
}
