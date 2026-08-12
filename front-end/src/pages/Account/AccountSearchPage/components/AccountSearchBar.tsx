import { Button, Icon, TextArea, WellContainer } from '@cfpb/design-system-react'
import { useNavigate } from '@tanstack/react-router'
import DOMPurify from 'dompurify'
import { useRef, type ReactElement } from 'react'
import './AccountSearchBar.scss'
interface AccountSearchBarProperties {
  initialValue?: string | null
  eventId: string | number
}

export const sanitizeAccountIdInput = (inputString: string | undefined): string => {
  if (inputString === undefined) return ''
  // Sanitize / strip all html tags from string
  return DOMPurify.sanitize(inputString, { ALLOWED_TAGS: [] })
}

export default function AccountSearchBar({
  initialValue = '',
  eventId
}: AccountSearchBarProperties): ReactElement {
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const navigate = useNavigate()

  const submitSearch = () => {
    // Get the value from the search input
    const searchString = inputRef.current?.value
    // Verify that the search value has changed
    if (searchString !== initialValue) {
      // Sanitize the search string
      const sanitizedSearchString = sanitizeAccountIdInput(searchString).replaceAll(
        ' ',
        ''
      )
      if (sanitizedSearchString === initialValue) {
        if (inputRef.current) inputRef.current.value = ''
      } else {
        const accountIds = [
          ...new Set(sanitizedSearchString.split(',').filter(item => item !== ''))
        ]
        // Navigate to account search page with account ids in querystring
        void navigate({
          resetScroll: false,
          to: '/events/$eventId/accounts',
          params: { eventId: String(eventId) },
          search: () => {
            return accountIds.length === 0
              ? {}
              : {
                  cons_acct_num: accountIds
                }
          }
        })
      }
    }
  }

  const handleReset = (event: React.BaseSyntheticEvent) => {
    event.preventDefault()
    if (inputRef.current) inputRef.current.value = ''
  }

  const handleSubmit = (event: React.SubmitEvent<HTMLFormElement>): void => {
    event.preventDefault()
    submitSearch()
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      submitSearch()
    }
  }

  return (
    <WellContainer className='account-search-container'>
      <form
        onSubmit={handleSubmit}
        onReset={handleReset}
        data-testid='account-search-bar'>
        <h3 data-testid='account-search-heading'>Find an account</h3>
        <p>
          {`Enter the account number, or numbers, you're looking for. To search for
        multiple accounts, ensure all account numbers are separated by commas.`}
        </p>
        <div className='o-search-input o-search-input--expandable-textarea'>
          <div className='o-search-input__input' key={initialValue ?? ''}>
            <label className='o-search-input__input-label' htmlFor='SearchInput'>
              <Icon name='search' />
            </label>
            <TextArea
              id='SearchInput'
              name='SearchInput'
              ref={inputRef}
              placeholder=''
              defaultValue={initialValue ?? ''}
              data-testid='account-search-input'
              onKeyDown={handleKeyDown}
            />
            <button
              aria-label='Clear search'
              title='Clear search'
              type='reset'
              data-testid='account-search-reset-button'>
              <Icon name='error' />
            </button>
          </div>
          <Button
            aria-label='Search for accounts'
            label='Search'
            type='submit'
            data-testid='account-search-submit-button'
          />
        </div>
      </form>
    </WellContainer>
  )
}
