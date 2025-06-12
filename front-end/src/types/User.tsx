import type EventMetadata from './EventMetadata'

export default interface User {
  is_admin: boolean
  username: string
  assigned_events: EventMetadata[]
}
