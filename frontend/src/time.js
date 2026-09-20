export function timeLeft(dueAt, now) {
  const minutes = Math.round((new Date(dueAt) - now) / 60000)
  const abs = Math.abs(minutes)
  const days = Math.floor(abs / 1440)
  const hours = Math.floor((abs % 1440) / 60)
  const rest = abs % 60
  let text = `${rest}m`
  if (days > 0) text = `${days}d ${hours}h`
  else if (hours > 0) text = `${hours}h ${rest}m`
  return minutes < 0 ? `${text} over` : `${text} left`
}

export function formatDue(dueAt, timeZone) {
  return new Date(dueAt).toLocaleString('en-CA', {
    timeZone,
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short',
  })
}
