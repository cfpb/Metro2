import BooleanFilter from '@src/components/Filters/BooleanFilter/BooleanFilter'

describe('BooleanFilter.cy.tsx', () => {
  it('mounts', () => {
    cy.mount(<BooleanFilter id='test-filter' />)
    // Should have 2 checkboxes, one with label "Has value" and other "No value"
  })
})
