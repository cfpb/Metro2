import { Alert, Button, List, ListItem } from '@cfpb/design-system-react'
import DownloadModal from '@src/components/Modal/DownloadModal'
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import DownloadErrorModal from '@src/pages/Evaluator/results/components/DownloadErrorModal'
import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import { fetchHitsForDownload } from '@src/queries/evaluatorHits'
import type AccountRecord from '@src/types/AccountRecord'
import type Event from '@src/types/Event'
import {
  downloadData,
  downloadFileFromURL,
  generateDownloadData
} from '@src/utils/downloads'
import { formatNumber } from '@src/utils/formatNumbers'
import type { ReactElement } from 'react'
import { useState } from 'react'

const FILTERED_LIMIT = 100_000
const REPRESENTATIVE_SAMPLE_COUNT = 20

export const downloadWarning: ReactElement = (
  <Alert
    message='Your requested download is too large'
    status='warning'
    className='u-mb15'
    data-testid='download-size-warning'>
    <>
      <div>
        {`At this time, the Metro 2 tool only supports downloads of ${formatNumber(FILTERED_LIMIT)} results. Instead, you can:`}
      </div>
      <List>
        <ListItem>Save a link to this evaluator&apos;s results</ListItem>
        <ListItem>Filter the results to get a smaller number of results</ListItem>
        <ListItem>{`Download the first ${formatNumber(FILTERED_LIMIT)} results`}</ListItem>
        <ListItem>
          Contact an administrator for help if you need the full results
        </ListItem>
      </List>
    </>
  </Alert>
)

interface EvaluatorDownloadInterface {
  rows: AccountRecord[]
  fields: string[]
  evaluatorId: string
  eventData: Event
  view: 'all' | 'sample'
  isFiltered: boolean
  totalHits: number
  currentHits: number
  query: EvaluatorSearch
}

type resultsScenarioType =
  | 'allResults'
  | 'representativeSample'
  | 'filteredOverLimit'
  | 'filteredMoreResults'
  | 'filtered'

export const getDownloadHeading = (resultsScenario: resultsScenarioType): string => {
  switch (resultsScenario) {
    case 'representativeSample': {
      return 'Download representative sample of results'
    }
    case 'allResults': {
      return 'Download all results'
    }
    default: {
      return 'Download filtered results'
    }
  }
}

export const getButtonText = (
  resultsScenario: resultsScenarioType,
  totalHits: number,
  currentHits: number
): string => {
  switch (resultsScenario) {
    case 'representativeSample': {
      return `Download ${REPRESENTATIVE_SAMPLE_COUNT} sample results`
    }
    case 'allResults': {
      return `Download ${formatNumber(totalHits)} results`
    }
    case 'filteredOverLimit': {
      return `Download first ${formatNumber(FILTERED_LIMIT)} results`
    }
    default: {
      return `Download ${formatNumber(currentHits)} results`
    }
  }
}

export default function EvaluatorDownloader({
  rows,
  fields,
  evaluatorId,
  eventData,
  view,
  isFiltered = false,
  totalHits,
  currentHits,
  query
}: EvaluatorDownloadInterface): ReactElement {
  const [isOpen, setIsOpen] = useState(false)
  const [isError, setIsError] = useState(false)

  // Determine which results to download based on the current situation.
  // Defaults to 'all results'.
  let resultsScenario: resultsScenarioType = 'allResults'

  if (view === 'sample' && totalHits > REPRESENTATIVE_SAMPLE_COUNT) {
    // If we're on the sample view and there are more results than shown here,
    // we're downloading a representative sample.
    resultsScenario = 'representativeSample'
  } else if (view === 'all' && isFiltered && currentHits < totalHits) {
    // If filters have been applied and they've reduced the number of records,
    // we're downloading filtered results & need to determine if there are more to fetch.
    if (currentHits > rows.length) {
      resultsScenario =
        currentHits > FILTERED_LIMIT ? 'filteredOverLimit' : 'filteredMoreResults'
    } else {
      resultsScenario = 'filtered'
    }
  }

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onCloseErrorModal = (): void => {
    setIsError(false)
  }

  const onDownload = async (): Promise<void> => {
    let dataToDownload

    switch (resultsScenario) {
      case 'allResults': {
        // Download pre-generated results file from server.
        const url = `/api/events/${eventData.id}/evaluator/${evaluatorId}/csv/`
        downloadFileFromURL(url)
        setIsOpen(false)
        return
      }
      case 'filteredOverLimit':
      case 'filteredMoreResults': {
        // Fetch more results from the server, up to the FILTERED_LIMIT
        try {
          dataToDownload = await fetchHitsForDownload(
            String(eventData.id),
            evaluatorId,
            {
              ...query,
              page_size:
                resultsScenario === 'filteredOverLimit'
                  ? FILTERED_LIMIT
                  : currentHits
            }
          )
        } catch {
          // If there's an error fetching results, close this modal and trigger an error one.
          setIsError(true)
          setIsOpen(false)
        }
        break
      }
      default: {
        // In other scenarios, we already have all the results in the table.
        dataToDownload = rows
      }
    }

    // Handle download for sample or filtered results
    if (Array.isArray(dataToDownload)) {
      // If there's an array of records, create a csv and initiate download.
      const fileName = `${eventData.name}_${evaluatorId}_${view === 'all' ? 'filtered' : 'sample'}.csv`
      const csv = generateDownloadData<AccountRecord>(
        fields,
        dataToDownload,
        M2_FIELD_NAMES
      )
      downloadData(csv, fileName)
    } else {
      // If there's no data to download, trigger the error modal.
      setIsError(true)
    }
    setIsOpen(false)
  }

  return (
    <div className='downloader'>
      <Button
        appearance='primary'
        label='Save results'
        iconRight='download'
        onClick={onClick}
        size='default'
        // disable the download button if there are no results for filters
        disabled={isFiltered && rows.length === 0}
        data-testid='evaluator-save-button'
      />
      <DownloadModal
        open={isOpen}
        onClose={onClose}
        onDownload={onDownload}
        title='Save results'
        copyText="Copy the link to this evaluator's results. Any filters you've applied will be included."
        downloadHeading={getDownloadHeading(resultsScenario)}
        buttonText={getButtonText(resultsScenario, totalHits, currentHits)}
        downloadContent={
          resultsScenario === 'filteredOverLimit' ? downloadWarning : null
        }
      />
      <DownloadErrorModal open={isError} onClose={onCloseErrorModal} />
    </div>
  )
}
