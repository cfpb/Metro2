import EvaluatorMetadataSection from '@src/pages/Evaluator/overview/components/Metadata'

describe('EvaluatorMetadataSection.cy.tsx', () => {
  it('should display populated metadata fields', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator',
      rationale: '<p>This evaluator checks for a mismatch between two fields.</p>',
      potential_harm: '<p>Description of potential harm.</p>',
      alternate_explanation: '',
      crrg_reference:
        '<p>Where to look in the CRRG:</p><ul><li>Page 2.3</li><li>Page 4.6</li></ul>'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)

    cy.findByTestId('metadata')
      .should('be.visible')
      .within(() => {
        // Metadata fields with content should be output
        cy.contains('h4', 'Rationale').should('exist')
        cy.findByTestId('rationale')
          .should('exist')
          .and('contain.html', metadata.rationale)
        cy.contains('h4', 'CRRG reference').should('exist')
        cy.findByTestId('crrg_reference').should(
          'contain.html',
          metadata.crrg_reference
        )
        cy.contains('h4', 'Potential harm').should('exist')
        cy.findByTestId('potential_harm').should(
          'contain.html',
          metadata.potential_harm
        )

        // Metadata fields without content should be skipped
        cy.contains('h4', 'Alternate explanation').should('not.exist')
        cy.findByTestId('alternate_explanation').should('not.exist')
      })
  })

  it('should display contribute call to action for admins', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator',
      rationale: 'This evaluator checks for a mismatch between two fields.',
      crrg_reference: 'Where to look in the CRRG.'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)
    cy.findByTestId('metadata-contribute-admin').should('be.visible')
    cy.findByTestId('metadata-contribute').should('not.exist')
    cy.findByTestId('no-metadata-contribute').should('not.exist')
  })

  it('should show no metadata call to action to non-admins', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator',
      rationale: '',
      crrg_reference: '',
      alternate_explanation: '',
      potential_harm: ''
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin={false} />)
    cy.findByTestId('no-metadata-contribute').should('be.visible')
    cy.findByTestId('metadata-contribute-admin').should('not.exist')
    cy.findByTestId('metadata-contribute').should('not.exist')
  })

  it('should show metadata call to action to non-admins', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator',
      rationale: '<p>This evaluator checks for a mismatch between two fields.</p>',
      potential_harm: '<p>Description of potential harm.</p>',
      alternate_explanation: '',
      crrg_reference:
        '<p>Where to look in the CRRG:</p><ul><li>Page 2.3</li><li>Page 4.6</li></ul>'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin={false} />)
    cy.findByTestId('metadata-contribute').should('be.visible')
    cy.findByTestId('metadata-contribute-admin').should('not.exist')
    cy.findByTestId('no-metadata-contribute').should('not.exist')
  })
})
