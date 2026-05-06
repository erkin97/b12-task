import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest'
import { ApiError, findBestFlight } from '../src/api'

describe('findBestFlight', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  test('parses a successful response', async () => {
    ;(fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        destination_city: 'Rome',
        dollars_per_km: 0.04,
        price_usd: 52,
        distance_km: 1434,
        fly_from_airport: 'STN',
        fly_to_airport: 'FCO',
      }),
    })

    const result = await findBestFlight('London', ['Rome'])
    expect(result.destination_city).toBe('Rome')
    expect(result.dollars_per_km).toBe(0.04)
  })

  test('throws ApiError on 4xx with backend error message', async () => {
    ;(fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({ error: 'No city found for: Nowheresville' }),
    })

    await expect(findBestFlight('Nowheresville', ['Rome'])).rejects.toThrow(ApiError)
  })
})
