import { Button } from '@/components/ui/Button'
import { ThemeToggle } from '@/components/ThemeToggle'
import { AppState } from '@/App'

interface WelcomePageProps {
  onCreateChat: () => void
  appState: AppState
  updateState: (updates: Partial<AppState>) => void
}

export function WelcomePage({ onCreateChat, appState, updateState }: WelcomePageProps) {
  const toggleTheme = () => {
    updateState({ theme: appState.theme === 'light' ? 'dark' : 'light' })
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="p-4 flex justify-end">
        <ThemeToggle theme={appState.theme} onToggle={toggleTheme} />
      </header>
      
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center space-y-8 max-w-md mx-auto px-4">
          <div className="space-y-4">
            <div className="mx-auto">
              <img 
                src="/assets/logo-light.png" 
                alt="RAGforge Logo" 
                className="w-lg h-lg mx-auto dark:hidden"
              />
              <img 
                src="/assets/logo-dark.png" 
                alt="RAGforge Logo" 
                className="w-lg h-lg mx-auto hidden dark:block"
              />
            </div>
            <h1 className="text-3xl font-bold text-foreground">
              Welcome
            </h1>
            <p className="text-muted-foreground text-lg">
              Your intelligent document chatbot powered by retrieval-augmented generation
            </p>
          </div>
          
          <Button 
            onClick={onCreateChat}
            size="lg"
            className="w-full max-w-xs"
          >
            Create New Chat
          </Button>
          
          <p className="text-sm text-muted-foreground">
            Built to support the Informatics degree at <a className="underline" href="https://www.its.ac.id">Institut Teknologi Sepuluh Nopember Surabaya</a>
          </p>
        </div>
      </div>
    </div>
  )
}
