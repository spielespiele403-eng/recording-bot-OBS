import type { Business, Service } from "@prisma/client";
import { createBooking, getSlots } from "./calcom.client.js";

export async function getAvailableSlots(
  business: Business,
  service: Service,
  range: { startTime: string; endTime: string },
) {
  const response = await getSlots(business.calcomApiKey, {
    eventTypeId: service.calcomEventTypeId,
    startTime: range.startTime,
    endTime: range.endTime,
    timeZone: business.timezone,
  });

  return Object.values(response.data).flat().map((slot) => slot.time);
}

export async function bookSlot(
  business: Business,
  service: Service,
  params: { startTime: string; customerName: string; customerPhone: string },
) {
  const response = await createBooking(business.calcomApiKey, {
    eventTypeId: service.calcomEventTypeId,
    start: params.startTime,
    attendee: {
      name: params.customerName,
      // Cal.com requires an attendee email; synthesize one since phone callers don't have one.
      email: `${params.customerPhone.replace(/[^0-9+]/g, "")}@phone-caller.invalid`,
      phoneNumber: params.customerPhone,
      timeZone: business.timezone,
    },
  });

  return response.data;
}

/** Public booking-page link for the missed-call-recovery SMS - points at the
 * business's general Cal.com page rather than one specific service/event type. */
export function getPublicBookingLink(business: Business) {
  return `https://cal.com/${business.calcomUsername}`;
}
