import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'
import Learn from './pages/Learn'
import Analytics from './pages/Analytics'
import Leaderboard from './pages/Leaderboard'
import Navbar from './components/Navbar'
import ChatBot from './components/ChatBot'

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-mesh">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/dashboard" element={<><Navbar /><Dashboard /></>} />
            <Route path="/learn" element={<><Navbar /><Learn /></>} />
            <Route path="/analytics" element={<><Navbar /><Analytics /></>} />
            <Route path="/leaderboard" element={<><Navbar /><Leaderboard /></>} />
          </Routes>
          <ChatBot />
        </div>
      </BrowserRouter>
    </AppProvider>
  )
}
