import { Alert, Button, List, ListItem } from '@cfpb/design-system-react'
import DownloadModal from '@src/components/Modal/DownloadModal'
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import { filterParams } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import type AccountRecord from '@src/types/AccountRecord'
import type Event from '@src/types/Event'
import { stringifySearchParams } from '@src/utils/customStringify'
import {
  downloadData,
  downloadFileFromURL,
  generateDownloadData
} from '@src/utils/downloads'
import { formatNumber } from '@src/utils/formatNumbers'
import type { ReactElement } from 'react'
import { useState } from 'react'

const FILTERED_LIMIT = 1_000_000
const SAMPLE_COUNT = 20

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

type resultsScenarioType = 'allResults' | 'sample' | 'filteredOverLimit' | 'filtered'

export const getDownloadHeading = (resultsScenario: resultsScenarioType): string => {
  switch (resultsScenario) {
    case 'sample': {
      return 'Download sample of results'
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
    case 'sample': {
      return `Download ${SAMPLE_COUNT} sample results`
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

  // Determine which results to download based on the current situation.
  // Defaults to 'all results'.
  let resultsScenario: resultsScenarioType = 'allResults'

  if (view === 'sample' && totalHits > SAMPLE_COUNT) {
    // If we're on the sample view and there are more results than shown here,
    // we're downloading a random sample.
    resultsScenario = 'sample'
  } else if (view === 'all' && isFiltered && currentHits < totalHits) {
    // If filters have been applied and reduced the number of hits,
    // we're downloading either all the filtered results
    // or the max number of filtered results that can be downloaded at once.
    resultsScenario = currentHits > FILTERED_LIMIT ? 'filteredOverLimit' : 'filtered'
  }

  const onClose = (): void => {
    setIsOpen(false)
  }

  const onClick = (): void => {
    setIsOpen(true)
  }

  const onDownload = () => {
    if (resultsScenario === 'sample') {
      const fileName = `${eventData.name}_${evaluatorId}_sample.csv`
      const csv = generateDownloadData<AccountRecord>(fields, rows, M2_FIELD_NAMES)
      downloadData(csv, fileName)
    } else {
      let url = `/api/events/${eventData.id}/evaluator/${evaluatorId}/csv/`
      if (resultsScenario.startsWith('filtered')) {
        // Remove any params that aren't filters
        const params = Object.fromEntries(
          Object.entries(query).filter(([key]) => filterParams.includes(key))
        )
        // Add a page_size param if we're over the download size limit
        if (resultsScenario === 'filteredOverLimit')
          params.page_size = FILTERED_LIMIT
        // Add search param querystring to the csv download URL
        url += stringifySearchParams(params)
      }
      downloadFileFromURL(url)
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
    </div>
  )
}
