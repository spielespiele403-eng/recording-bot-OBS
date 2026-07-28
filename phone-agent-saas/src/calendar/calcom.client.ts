import type {
  CalcomCreateBookingRequest,
  CalcomCreateBookingResponse,
  CalcomSlotsResponse,
} from "../types/calcom.types.js";

const CALCOM_API_BASE = "https://api.cal.com/v2";

async function calcomFetch<T>(apiKey: string, path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${CALCOM_API_BASE}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Cal.com API error ${response.status} on ${path}: ${body}`);
  }

  return (await response.json()) as T;
}

export function getSlots(
  apiKey: string,
  params: { eventTypeId: number; startTime: string; endTime: string; timeZone: string },
) {
  const query = new URLSearchParams({
    eventTypeId: String(params.eventTypeId),
    startTime: params.startTime,
    endTime: params.endTime,
    timeZone: params.timeZone,
  });

  return calcomFetch<CalcomSlotsResponse>(apiKey, `/slots?${query.toString()}`);
}

export function createBooking(apiKey: string, booking: CalcomCreateBookingRequest) {
  return calcomFetch<CalcomCreateBookingResponse>(apiKey, "/bookings", {
    method: "POST",
    body: JSON.stringify(booking),
  });
}
