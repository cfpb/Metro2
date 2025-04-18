import React, { useState } from 'react';
import { Button, TextInput } from 'design-system-react'

interface Properties {
      url: string
    }

export default function CopyUrl() {
  const [copySuccess, setCopySuccess] = useState('Copy URL');
  const [labelText, setLabelText] = useState(window.location.href);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopySuccess('URL Copied!');
      setLabelText('URL Copied!')
    } catch (err) {
      setCopySuccess('Failed to copy URL');
    }
  };
  return(
    <div className="o-form__input-w-btn">
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
            label={copySuccess}
            size='default'
            onClick={copyToClipboard}
            />
        </div>
    </div>
    )
}