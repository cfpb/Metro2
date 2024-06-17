import type { ReactElement, ReactNode } from 'react'
import ReactDom from 'react-dom'
import './Modal.less'

interface ModalProperties {
  open: boolean
  children?: ReactNode
}

export function Modal({
  children,
  open
}: ModalProperties & React.HTMLAttributes<HTMLDivElement>): ReactElement | null {
  if (!open) return null
  return ReactDom.createPortal(
    <div>
      <div className='modal-overlay' />
      <div className='modal'>{children}</div>
    </div>,
    document.body
  )
}

interface ModalFooterProps {
  children: React.ReactNode
}

export function ModalFooter({
  children
}: ModalFooterProps & React.HTMLAttributes<HTMLDivElement>): ReactElement {
  return (
    <div className='modal-footer' data-testid='modalFooter'>
      {children}
    </div>
  )
}
