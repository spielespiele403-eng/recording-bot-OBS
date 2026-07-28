// Minimal shapes for the subset of the Cal.com v2 API this project calls.
// See https://cal.com/docs/api-reference/v2 for the full schema.

export interface CalcomSlot {
  time: string; // ISO 8601
}

export interface CalcomSlotsResponse {
  status: "success" | "error";
  data: Record<string, CalcomSlot[]>; // keyed by date, e.g. "2026-08-01"
}

export interface CalcomCreateBookingRequest {
  eventTypeId: number;
  start: string; // ISO 8601
  attendee: {
    name: string;
    email: string;
    phoneNumber?: string;
    timeZone: string;
  };
  metadata?: Record<string, string>;
}

export interface CalcomBooking {
  id: number;
  uid: string;
  start: string;
  end: string;
  status: string;
}

export interface CalcomCreateBookingResponse {
  status: "success" | "error";
  data: CalcomBooking;
}
