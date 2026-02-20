import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AnalysisPage from './pages/AnalysisPage'
import DashboardPage from './pages/DashboardPage'
import DetailPage from './pages/DetailPage'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="/dashboard/:jobId" element={<DashboardPage />} />
        <Route path="/detail/:username" element={<DetailPage />} />
      </Routes>
    </Layout>
  )
}

export default App
