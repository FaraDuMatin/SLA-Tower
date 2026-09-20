import { formatDue, timeLeft } from '../time'

export function TicketCard({ ticket, now }) {
  return (
    <a className={`card ${ticket.bucket}`} href={ticket.jira_url} target="_blank" rel="noreferrer">
      <div className="card-top">
        <span className="key">{ticket.jira_key || `#${ticket.id}`}</span>
        <span className="tag">{ticket.priority}</span>
        <span className="tag">{ticket.country}</span>
      </div>
      <p>{ticket.title}</p>
      <div className="card-due">
        <strong>{timeLeft(ticket.due_at, now)}</strong>
        <span>{formatDue(ticket.due_at, ticket.timezone)}</span>
      </div>
    </a>
  )
}
