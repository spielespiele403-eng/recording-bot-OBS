import type { BusinessWithServices } from "../../businesses/business.service.js";
import { bookSlot } from "../../calendar/calcom.service.js";
import { createAppointment } from "../../appointments/appointment.repository.js";
import { logCallOutcome } from "../../calls/call.service.js";

export async function bookAppointment(
  business: BusinessWithServices,
  args: { serviceName: string; slotStart: string; customerName: string; customerPhone: string },
  context: { vapiCallId: string; callId: string },
): Promise<string> {
  const service = business.services.find(
    (candidate) => candidate.name.toLowerCase() === args.serviceName.toLowerCase(),
  );

  if (!service) {
    return JSON.stringify({
      error: `Unbekannte Leistung "${args.serviceName}". Verfügbare Leistungen: ${business.services
        .map((s) => s.name)
        .join(", ")}`,
    });
  }

  const booking = await bookSlot(business, service, {
    startTime: args.slotStart,
    customerName: args.customerName,
    customerPhone: args.customerPhone,
  });

  await createAppointment({
    businessId: business.id,
    callId: context.callId,
    serviceId: service.id,
    calcomBookingId: String(booking.id),
    customerName: args.customerName,
    customerPhone: args.customerPhone,
    startTime: new Date(booking.start),
    endTime: new Date(booking.end),
  });

  await logCallOutcome(context.vapiCallId, "BOOKED");

  return JSON.stringify({
    confirmed: true,
    serviceName: service.name,
    startTime: booking.start,
  });
}
