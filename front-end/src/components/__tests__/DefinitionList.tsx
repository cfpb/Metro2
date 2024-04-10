import { render, screen, within } from '@testing-library/react'
import DefinitionList from '../DefinitionList/DefinitionList'

const definitionListData = [
  { term: 'CFPB', definition: 'Consumer Financial Protection Bureau' },
  { term: 'FDIC', definition: 'Federal Deposit Insurance Corporation' },
  { term: 'NCUA', definition: 'National Credit Union Administration' }
]

describe('<DefinitionList />', () => {
  it('displays list of items', () => {
    render(<DefinitionList items={definitionListData} />)
    const definitionListElements = screen.getAllByTestId('dl-item')
    expect(definitionListElements).toHaveLength(3)
    for (const [index, element] of definitionListElements.entries()) {
      const data = definitionListData[index]
      expect(within(element).getByRole('term')).toHaveTextContent(data.term)
      expect(within(element).getByRole('definition')).toHaveTextContent(
        data.definition
      )
    }
  })
})
