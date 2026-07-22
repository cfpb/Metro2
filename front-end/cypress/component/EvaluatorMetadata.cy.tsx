import EvaluatorMetadataSection from '@src/pages/Evaluator/overview/components/Metadata'
import { formatDate } from '@src/utils/formatDates'

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
        '<p>Where to look in the CRRG:</p><ul><li>Page 2.3</li><li>Page 4.6</li></ul>',

      interpret_fields_last_modified: '7/7/26'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)

    cy.get('.evaluate-expandable')
      .should('be.visible')
      .within(() => {
        cy.get('.o-expandable__target').click()

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

        // Last updated date should be populated
        cy.findByTestId('interpret-fields-last-modified-date')
          .should('exist')
          .and(
            'contain',
            formatDate(metadata.interpret_fields_last_modified, 'fullText')
          )
      })
  })

  it('should display no metadata note if no metadata fields populated', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)

    cy.get('.evaluate-expandable')
      .should('be.visible')
      .within(() => {
        cy.get('.o-expandable__target').click()

        cy.findByTestId('no-metadata-message').should('exist')

        // Last updated date should not be populated
        cy.findByTestId('interpret-fields-last-modified-date').should('not.exist')

        // Metadata fields without content should be skipped
        cy.contains('h4', 'Alternate explanation').should('not.exist')
        cy.findByTestId('alternate_explanation').should('not.exist')
        cy.contains('h4', 'Rationale').should('not.exist')
        cy.findByTestId('rationale').should('not.exist')
        cy.contains('h4', 'CRRG reference').should('not.exist')
        cy.findByTestId('crrg_reference').should('not.exist')
        cy.contains('h4', 'Potential harm').should('not.exist')
        cy.findByTestId('potential_harm').should('not.exist')
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
    cy.get('.evaluate-expandable').within(() => {
      cy.get('.o-expandable__target').click()
      cy.findByTestId('metadata-contribute-admin').should('be.visible')
      cy.findByTestId('metadata-contribute').should('not.exist')
      cy.findByTestId('no-metadata-contribute').should('not.exist')
    })
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
    cy.get('.evaluate-expandable').within(() => {
      cy.get('.o-expandable__target').click()
      cy.findByTestId('no-metadata-contribute').should('be.visible')
      cy.findByTestId('metadata-contribute-admin').should('not.exist')
      cy.findByTestId('metadata-contribute').should('not.exist')
    })
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
    cy.get('.evaluate-expandable').within(() => {
      cy.get('.o-expandable__target').click()
      cy.findByTestId('metadata-contribute').should('be.visible')
      cy.findByTestId('metadata-contribute-admin').should('not.exist')
      cy.findByTestId('no-metadata-contribute').should('not.exist')
    })
  })

  it('should not show additional notes expandable if not populated', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator',
      additional_notes: '',
      additional_notes_last_modified: ''
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin={false} />)
    cy.get('.additional-notes-expandable').should('not.exist')
  })

  it('should show additional notes expandable if populated', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      fields_used: ['acct_stat', 'acct_type'],
      long_description: 'Long description of evaluator',
      additional_notes: '<h4>Note category</h4><p>Lorem ipsum dolor</p>',
      additional_notes_last_modified: '7/7/26'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin={false} />)
    cy.get('.additional-notes-expandable')
      .should('be.visible')
      .within(() => {
        cy.findByTestId('additional-notes')
          .should('exist')
          .and('contain.html', metadata.additional_notes)
        cy.findByTestId('additional-notes-last-modified-date')
          .should('exist')
          .and(
            'contain',
            formatDate(metadata.additional_notes_last_modified, 'fullText')
          )
      })
  })
})
