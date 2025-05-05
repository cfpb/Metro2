import { Button } from 'design-system-react'
import type { ReactElement } from 'react'
import { useState } from 'react'

export default function CopyUrl(): ReactElement {
  const [copySuccess, setCopySuccess] = useState('Copy URL')

  const onClick = async (): Promise<void> => {
    try {
      await navigator.clipboard.writeText(window.location.href)
      setCopySuccess('URL Copied!')
      setTimeout(() => {
        setCopySuccess('Copy URL')
      }, 2000)
    } catch {
      setCopySuccess('Failed to copy URL')
      setTimeout(() => {
        setCopySuccess('Copy URL')
      }, 2000)
    }
  }

  return (
    <div>
      <Button
        appearance='primary'
        label={copySuccess}
        size='default'
        onClick={onClick}
      />
    </div>
  )
}
