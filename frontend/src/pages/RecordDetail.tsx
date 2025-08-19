import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/axios'

function formatValue(key: string, value: any) {
  const s = String(value ?? '')
  if (key === 'student_name') {
    const m = s.match(/^(.*?)(Enrollment\s*No\s*:\s*.+)$/i)
    if (m) {
      const before = m[1].trim()
      const enroll = m[2].trim().replace(/^\(+|\)+$/g, '').trim()
      return `${before} (${enroll})`
    }
  }
  return s
}

const IMPORTANT_KEYS = [
  'student_name',
  'registration_no',
  'degree',
  'date_of_birth',
  'year',
  'classification',
]

export default function RecordDetail() {
  const { id } = useParams()
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showRaw, setShowRaw] = useState(false)

  const imageUrl = useMemo(() => {
    const base = (api.defaults.baseURL || '').replace(/\/$/, '')
    return `${base}/certificates/${id}/image`
  }, [id])

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get(`/certificates/${id}`)
        setData(res.data)
      } catch (err: any) {
        setError(err?.response?.data?.error || 'Failed to load record')
      } finally {
        setLoading(false)
      }
    })()
  }, [id])

  if (loading) return <p style={{ padding: 16 }}>Loading...</p>
  if (error) return <p style={{ padding: 16, color: 'red' }}>{error}</p>
  if (!data) return <p style={{ padding: 16 }}>No data.</p>

  // Map fields from array into a dict for quick lookup
  const fieldMap: Record<string, any> = {}
  for (const f of data.fields || []) {
    if (typeof f?.key === 'string') fieldMap[f.key] = f.value
  }
  const hasImportant = IMPORTANT_KEYS.some((k) => fieldMap[k])

  return (
    <div style={{ padding: 16 }}>
      <h2>Record #{data.id}</h2>
      <div style={{ display: 'flex', gap: 24, alignItems: 'flex-start' }}>
        <img src={imageUrl} alt={`Certificate ${data.id}`} style={{ maxWidth: 400, border: '1px solid #ddd' }} />
        <div style={{ flex: 1 }}>
          <h3>Extracted Fields</h3>
          {hasImportant ? (
            <table style={{ borderCollapse: 'collapse', width: '100%', maxWidth: 600 }}>
              <tbody>
                {IMPORTANT_KEYS.map((k) => (
                  fieldMap[k] ? (
                    <tr key={k}>
                      <td style={{ border: '1px solid #444', padding: '8px', fontWeight: 600, textTransform: 'capitalize', width: '35%' }}>
                        {k.replaceAll('_', ' ')}
                      </td>
                      <td style={{ border: '1px solid #444', padding: '8px' }}>{formatValue(k, fieldMap[k])}</td>
                    </tr>
                  ) : null
                ))}
              </tbody>
            </table>
          ) : (
            <p>No structured fields found.</p>
          )}

          {data.fields?.length ? (
            <div style={{ marginTop: 16 }}>
              <button onClick={() => setShowRaw((s) => !s)} style={{ padding: '6px 10px' }}>
                {showRaw ? 'Hide raw' : 'Show raw'}
              </button>
              {showRaw && (
                <ul>
                  {data.fields.map((f: any, idx: number) => (
                    <li key={idx}>
                      <strong>{f.key}:</strong> {f.value}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
