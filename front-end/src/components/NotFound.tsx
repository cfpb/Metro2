import type { ReactElement } from 'react'
import { Link } from '@tanstack/react-router'

export default function NotFound():  ReactElement {
    return (
        <div className='error-container content-row' data-testid='error-container'>
            <div data-testid='error-message' className='error-message'>
                <h2 data-testid='title' className='h1'>
                    This page doesn&apos;t exist.
                </h2>
                <p data-testid='description'>
                    We can&apos;t find the page you&apos;re looking for.
                    If you believe you are seeing this in error
                    double check that the URL is correct.
                    If you need additional help, please contact an
                    administrator for help.
                </p>
                <div className="m-btn-group">
                    <Link data-testid='button' to='/' className='a-btn a-btn__full-on-xs'>Back to Metro 2 homepage</Link>
                    <Link to='/' className='a-btn a-btn__link a-btn__full-on-xs'>Contact an administrator
                        <svg xmlns="http://www.w3.org/2000/svg" className="cf-icon-svg cf-icon-svg__email a-btn__link" viewBox="0 0 17 19">
                            <path d="M16.417 6.823v7.809a.557.557 0 0 1-.556.555H1.139a.557.557 0 0 1-.556-.555V6.823a.557.557 0 0 1 .556-.555h14.722a.557.557 0 0 1 .556.555m-14.722.92v6.146l4.463-2.89zm12.223-.364H3.082l4.463 3.257a1.777 1.777 0 0 0 1.91 0zM3.45 14.076h10.096L9.864 11.69a2.926 2.926 0 0 1-2.728 0zm11.855-.184v-6.15L10.842 11z" />
                        </svg>
                    </Link>
                </div>
            </div>
        </div>
    )
}