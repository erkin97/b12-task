import { useState } from 'react'
import { ApiError, findBestFlight, type BestFlight } from './api'
import { ResultCard } from './ResultCard'
import { SearchForm } from './SearchForm'

export default function App() {
  const [result, setResult] = useState<BestFlight | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(origin: string, destinations: string[]) {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const best = await findBestFlight(origin, destinations)
      setResult(best)
    } catch (e) {
      setError(e instanceof ApiError ? e.message : 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="max-w-md mx-auto space-y-6">
        <header>
          <h1 className="text-2xl font-bold text-slate-900">Flight Optimizer</h1>
          <p className="text-sm text-slate-600 mt-1">
            Find the destination with the cheapest dollars per kilometer.
          </p>
        </header>
        <SearchForm onSubmit={handleSubmit} loading={loading} />
        {error && (
          <div className="border border-red-200 bg-red-50 text-red-800 rounded-md p-3 text-sm">
            {error}
          </div>
        )}
        {result && <ResultCard flight={result} />}
      </div>
    </main>
  )
}
