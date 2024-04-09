import type { NotFoundError } from '@tanstack/react-router'
import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import errors from './ErrorList'

export default function NotFound({ data }: NotFoundError): ReactElement {
  // Todo: use the data value that is optionally passed in
  // to the NotFound component to determine which not found content to show.
  // Data value should reflect the request that threw the not found error:
  // 'account', 'evaluator', or 'event'
  // Default to the generic not found content if data is undefined
  console.log(data)

  // the "event" message is the default not found error message
  let eventError = errors.event

  const errorType = data?.data

  if (errorType in errors){
    eventError = errors[errorType as keyof typeof errors]
  }

  return (
  <div className='error-container content-row' data-testid='error-container'>
    <div data-testid='error-message' className='error-message'>
      <h2 data-testid='title' className='h1'>
        {eventError.title}
      </h2>
      <p data-testid='description'>
        {eventError.description}
      </p>
      <div className='m-btn-group'>
        <Link data-testid='button' to='/' className='a-btn a-btn__full-on-xs'>
          {eventError.cta1}
        </Link>
        <Link to='/' className='a-btn a-btn__link a-btn__full-on-xs'>
        {eventError.cta2}
          <svg
            xmlns='http://www.w3.org/2000/svg'
            className='cf-icon-svg cf-icon-svg__email a-btn__link'
            viewBox='0 0 17 19'>
            <path d='M16.417 6.823v7.809a.557.557 0 0 1-.556.555H1.139a.557.557 0 0 1-.556-.555V6.823a.557.557 0 0 1 .556-.555h14.722a.557.557 0 0 1 .556.555m-14.722.92v6.146l4.463-2.89zm12.223-.364H3.082l4.463 3.257a1.777 1.777 0 0 0 1.91 0zM3.45 14.076h10.096L9.864 11.69a2.926 2.926 0 0 1-2.728 0zm11.855-.184v-6.15L10.842 11z' />
          </svg>
        </Link>
      </div>
    </div>
  </div>
  )
}