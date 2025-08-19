import './App.css'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Upload from './pages/Upload'
import Records from './pages/Records'
import RecordDetail from './pages/RecordDetail'

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: 12, borderBottom: '1px solid #eee' }}>
        <Link to="/" style={{ marginRight: 12 }}>Upload</Link>
        <Link to="/records">Records</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/records" element={<Records />} />
        <Route path="/records/:id" element={<RecordDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
