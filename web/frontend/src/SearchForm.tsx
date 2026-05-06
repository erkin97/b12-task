import { useState, type FormEvent, type KeyboardEvent } from 'react'

type Props = {
  onSubmit: (origin: string, destinations: string[]) => void
  loading: boolean
}

export function SearchForm({ onSubmit, loading }: Props) {
  const [origin, setOrigin] = useState('')
  const [destInput, setDestInput] = useState('')
  const [destinations, setDestinations] = useState<string[]>([])

  function commitDest() {
    const trimmed = destInput.trim()
    if (trimmed && !destinations.includes(trimmed)) {
      setDestinations([...destinations, trimmed])
    }
    setDestInput('')
  }

  function onDestKey(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault()
      commitDest()
    } else if (e.key === 'Backspace' && !destInput && destinations.length) {
      setDestinations(destinations.slice(0, -1))
    }
  }

  function removeDest(d: string) {
    setDestinations(destinations.filter((x) => x !== d))
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (origin.trim() && destinations.length) {
      onSubmit(origin.trim(), destinations)
    }
  }

  const canSubmit = origin.trim().length > 0 && destinations.length > 0 && !loading

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">From</label>
        <input
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
          placeholder="London"
          className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-slate-400"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">To</label>
        <div className="flex flex-wrap items-center gap-2 px-2 py-2 border border-slate-300 rounded-md focus-within:ring-2 focus-within:ring-slate-400">
          {destinations.map((d) => (
            <span
              key={d}
              className="inline-flex items-center gap-1 bg-slate-100 text-slate-800 rounded-md px-2 py-1 text-sm"
            >
              {d}
              <button
                type="button"
                onClick={() => removeDest(d)}
                aria-label={`Remove ${d}`}
                className="text-slate-500 hover:text-slate-800"
              >
                x
              </button>
            </span>
          ))}
          <input
            value={destInput}
            onChange={(e) => setDestInput(e.target.value)}
            onKeyDown={onDestKey}
            onBlur={commitDest}
            placeholder={destinations.length === 0 ? 'Paris' : ''}
            className="flex-1 min-w-[8rem] px-1 focus:outline-none"
          />
        </div>
        <p className="text-xs text-slate-500 mt-1">Press Enter or comma to add</p>
      </div>
      <button
        type="submit"
        disabled={!canSubmit}
        className="w-full bg-slate-800 text-white py-2 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-900"
      >
        {loading ? 'Finding...' : 'Find best flight'}
      </button>
    </form>
  )
}
