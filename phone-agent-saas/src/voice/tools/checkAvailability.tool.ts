import type { BusinessWithServices } from "../../businesses/business.service.js";
import { getAvailableSlots } from "../../calendar/calcom.service.js";

export async function checkAvailability(
  business: BusinessWithServices,
  args: { serviceName: string; startDate: string; endDate: string },
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

  const slots = await getAvailableSlots(business, service, {
    startTime: `${args.startDate}T00:00:00.000Z`,
    endTime: `${args.endDate}T23:59:59.999Z`,
  });

  return JSON.stringify({ serviceName: service.name, availableSlots: slots });
}
