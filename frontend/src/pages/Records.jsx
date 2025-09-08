import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios.js'

export default function Records() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/certificates')
        setRecords(res.data?.certificates || [])
      } catch (err) {
        setError(err?.response?.data?.error || 'Failed to load records')
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  if (loading) return <p style={{ padding: 16 }}>Loading...</p>
  if (error) return <p style={{ padding: 16, color: 'red' }}>{error}</p>

  return (
    <div style={{ padding: 16 }}>
      <h2>Records</h2>
      {records.length === 0 ? (
        <p>No records yet.</p>
      ) : (
        <ul>
          {records.map(r => (
            <li key={r.id}>
              <Link to={`/records/${r.id}`}>#{r.id}</Link> — {r.summary || r.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
