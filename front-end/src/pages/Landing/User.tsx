import type { EventMetadata } from 'pages/Event/Event'

export default interface User {
  is_admin: boolean
  username: string
  assigned_events: EventMetadata[]
}
