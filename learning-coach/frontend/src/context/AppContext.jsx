import { createContext, useContext, useState } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [userId] = useState(() => {
    let id = localStorage.getItem('lc_uid')
    if (!id) { id = 'u_' + Math.random().toString(36).slice(2, 10); localStorage.setItem('lc_uid', id) }
    return id
  })
  const [currentTopic, setCurrentTopic] = useState('Machine Learning')
  const [profile, setProfile] = useState(null)
  const [analytics, setAnalytics] = useState(null)

  return (
    <AppContext.Provider value={{ userId, currentTopic, setCurrentTopic, profile, setProfile, analytics, setAnalytics }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
