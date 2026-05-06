import { z } from 'zod'

const BestFlightSchema = z.object({
  destination_city: z.string(),
  dollars_per_km: z.number(),
  price_usd: z.number(),
  distance_km: z.number(),
  fly_from_airport: z.string(),
  fly_to_airport: z.string(),
})

const ErrorSchema = z.object({ error: z.string() })

export type BestFlight = z.infer<typeof BestFlightSchema>

export class ApiError extends Error {}

export async function findBestFlight(
  origin: string,
  destinations: string[],
): Promise<BestFlight> {
  const resp = await fetch('/api/best-flight', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ origin, destinations }),
  })
  const body = await resp.json()
  if (!resp.ok) {
    const parsed = ErrorSchema.safeParse(body)
    throw new ApiError(parsed.success ? parsed.data.error : `HTTP ${resp.status}`)
  }
  return BestFlightSchema.parse(body)
}
