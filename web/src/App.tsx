import { useState, useEffect } from 'react'
import { WelcomePage } from '@/components/WelcomePage'
import { ChatDashboard } from '@/components/ChatDashboard'

export interface Collection {
  id: string
  name: string
  description: string
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
}

export interface AppState {
  theme: 'light' | 'dark'
  collections: Collection[]
  selectedCollection: Collection | null
  messages: Message[]
  isLoading: boolean
}

function App() {
  const [currentView, setCurrentView] = useState<'welcome' | 'chat'>('welcome')
  const [appState, setAppState] = useState<AppState>({
    theme: 'light',
    collections: [],
    selectedCollection: null,
    messages: [{
      role: 'assistant',
      content: '👋 Welcome to our chatbot! Please select a collection to begin.'
    }],
    isLoading: false
  })

  useEffect(() => {
    // Apply theme to document
    if (appState.theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [appState.theme])

  const updateState = (updates: Partial<AppState>) => {
    setAppState(prev => ({ ...prev, ...updates }))
  }

  return (
    <>
      {currentView === 'welcome' ? (
        <WelcomePage 
          onCreateChat={() => setCurrentView('chat')}
          appState={appState}
          updateState={updateState}
        />
      ) : (
        <ChatDashboard 
          onBack={() => setCurrentView('welcome')}
          appState={appState}
          updateState={updateState}
        />
      )}
    </>
  )
}

export default App
