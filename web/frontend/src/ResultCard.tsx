import type { BestFlight } from './api'

export function ResultCard({ flight }: { flight: BestFlight }) {
  return (
    <div className="border border-slate-300 rounded-md p-4 bg-white">
      <div className="text-sm text-slate-500">Best destination</div>
      <div className="text-2xl font-semibold text-slate-900">{flight.destination_city}</div>
      <div className="text-3xl font-bold text-slate-900 mt-2">
        ${flight.dollars_per_km.toFixed(2)}/km
      </div>
      <div className="text-sm text-slate-600 mt-3">
        ${flight.price_usd.toFixed(0)} over {flight.distance_km.toFixed(0)} km
      </div>
      <div className="text-xs text-slate-500 mt-1">
        {flight.fly_from_airport} to {flight.fly_to_airport}
      </div>
    </div>
  )
}
