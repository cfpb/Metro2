import { useNavigate } from '@tanstack/react-router'
import { Pagination } from 'design-system-react'
import type { ReactElement } from 'react'

interface EvaluatorPaginationData {
  pageCount: number
  page: number | undefined
}

export default function EvaluatorResultsPagination({
  pageCount,
  page = 1
}: EvaluatorPaginationData): ReactElement {
  const navigate = useNavigate()

  const onClickGo = (pageNum: number): void => {
    if (pageNum > pageCount) return
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev => ({ ...prev, page: pageNum })
    })
  }

  const onClickNext = (): void => {
    if (page === pageCount) return
    void navigate({
      resetScroll: false,
      to: '.',
      search: prev => ({
        ...prev,
        page: (typeof prev.page === 'number' ? prev.page : 1) + 1
      })
    })
  }

  const onClickPrevious = (): void => {
    if (page === 1) return
    void navigate({
      resetScroll: false,

      to: '.',
      search: prev => ({ ...prev, page: (prev.page ?? 1) - 1 })
    })
  }

  return (
    <div className=''>
      <Pagination
        page={page}
        pageCount={pageCount}
        onClickGo={onClickGo}
        onClickNext={onClickNext}
        onClickPrevious={onClickPrevious}
      />
    </div>
  )
}
