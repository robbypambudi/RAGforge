import { useEffect } from 'react'
import { BookOpen } from 'lucide-react'
import { AppState, Collection } from '@/App'

const BACKEND_URL = 'http://localhost:8000'

interface CollectionSelectorProps {
  appState: AppState
  updateState: (updates: Partial<AppState>) => void
}

export function CollectionSelector({ appState, updateState }: CollectionSelectorProps) {
  const { collections, selectedCollection } = appState

  useEffect(() => {
    fetchCollections()
  }, [])

  const fetchCollections = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/collection?page=1&collection_name&vectordb_collection_name`)
      const data = await response.json()
      
      console.log('API Response:', data) // Debug log
      
      if (data.status === 'success' && data.data) {
        const fetchedCollections = data.data.map((col: any) => ({
          id: col.id,
          name: col.collection_name,
          description: col.description
        }))
        console.log('Fetched collections:', fetchedCollections) // Debug log
        updateState({ collections: fetchedCollections })
      }
    } catch (error) {
      console.error('Failed to fetch collections:', error)
    }
  }

  const handleCollectionChange = (collection: Collection) => {
    updateState({ 
      selectedCollection: collection,
      messages: [{
        role: 'assistant',
        content: '👋 Welcome to our chatbot! Please select a collection to begin.'
      }]
    })
  }

  return (
    <div className="w-80 border-r bg-muted/30 p-4">
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-5 h-5" />
          <h2 className="font-semibold">Collections</h2>
        </div>
        
        {selectedCollection && (
          <div className="p-3 bg-primary/10 rounded-lg border">
            <h3 className="font-medium text-sm text-primary">{selectedCollection.name}</h3>
            <p className="text-xs text-muted-foreground mt-1">{selectedCollection.description}</p>
          </div>
        )}
        
        <div className="space-y-2">
          {collections.map((collection) => (
            <button
              key={collection.id}
              onClick={() => handleCollectionChange(collection)}
              className={`w-full text-left p-3 rounded-lg border transition-colors ${
                selectedCollection?.id === collection.id
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-background hover:bg-accent'
              }`}
            >
              <div className="font-medium text-sm">{collection.name}</div>
              <div className="text-xs opacity-70 mt-1">{collection.description}</div>
            </button>
          ))}
        </div>
        
        {collections.length === 0 && (
          <div className="text-center text-muted-foreground text-sm py-8">
            No collections available
          </div>
        )}
      </div>
    </div>
  )
}
