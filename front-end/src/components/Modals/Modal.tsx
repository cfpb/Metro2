import type { ReactElement, ReactNode } from 'react'
import { useEffect, useRef } from 'react'
import './Modal.less'

interface ModalProperties {
  children?: ReactNode
  open: boolean
}

const handleKeyDown = (e: KeyboardEvent): void => {
  if (e.key !== 'Escape') return
  e.preventDefault()
}

export function Modal({
  children,
  open
}: ModalProperties & React.HTMLAttributes<HTMLDivElement>): ReactElement | null {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const openModal = (): void => {
    dialogRef.current?.showModal()
  }
  const closeModal = (): void => {
    dialogRef.current?.close()
  }
  useEffect(() => {
    if (open) {
      openModal()
    } else {
      closeModal()
    }
  }, [open])

  // Don't close dialog when escape key is pressed
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  return (
    <dialog className='modal' ref={dialogRef}>
      <div className='modal-wrapper'>
        <div className='modal-contents'>
          <div>{children}</div>
        </div>
      </div>
    </dialog>
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
