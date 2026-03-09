import { Button } from '@cfpb/design-system-react'
import type { ReactElement } from 'react'
import { useState } from 'react'

export default function CopyUrl(): ReactElement {
  const [copySuccess, setCopySuccess] = useState('Copy URL')

  const onClick = async (): Promise<void> => {
    try {
      await navigator.clipboard.writeText(globalThis.location.href)
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
        data-testid='copyButton'
        appearance='primary'
        label={copySuccess}
        size='default'
        // eslint-disable-next-line @typescript-eslint/no-misused-promises
        onClick={onClick}
      />
    </div>
  )
}
