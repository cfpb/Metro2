import { useState } from 'react';
import type { ReactElement } from 'react'
import { Button, TextInput } from 'design-system-react'

interface CopyUrlInterface {
      url: string
    }

export default function CopyUrl({}: CopyUrlInterface): ReactElement {
  // const [copySuccess, setCopySuccess] = useState('Copy URL');
  const [labelText, setLabelText] = useState(window.location.href);

  const onClickCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      // setCopySuccess('URL Copied!');
      setLabelText('URL Copied!')
    } catch {
      // setCopySuccess('Failed to copy URL');
    }
  };
  return(
    <div className="o-form__input-w-btn o-form_fieldset">
        <div className="o-form__input-w-btn_input-container">
            <div className="m-btn-inside-input">
            <TextInput
                id="CopyURLText"
                name=""
                type="text"
                value={labelText}
            />
            </div>
        </div>
        <div className="o-form__input-w-btn_btn-container">
            <Button
            appearance="primary"
            label="Copy URL" // or use {copySuccess}  
            size='default'
            onClick={onClickCopyToClipboard}
            />
        </div>
    </div>
    )
}