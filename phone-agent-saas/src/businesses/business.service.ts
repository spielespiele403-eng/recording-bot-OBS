import type { Business, Service } from "@prisma/client";

export type BusinessWithServices = Business & { services: Service[] };

export type OpeningHoursByDay = Record<string, Array<{ start: string; end: string }>>;

export type FaqEntry = { question: string; answer: string };

export function parseBusinessHours(business: Business): OpeningHoursByDay {
  return JSON.parse(business.businessHours) as OpeningHoursByDay;
}

export function parseFaq(business: Business): FaqEntry[] {
  return business.faq ? (JSON.parse(business.faq) as FaqEntry[]) : [];
}

/** Renders the business's config into a compact block the Vapi assistant's
 * system prompt / get_business_info tool result can use, regardless of industry. */
export function getBusinessContext(business: BusinessWithServices) {
  return {
    name: business.name,
    industry: business.industry,
    timezone: business.timezone,
    businessHours: parseBusinessHours(business),
    faq: parseFaq(business),
    services: business.services.map((service) => ({
      name: service.name,
      durationMinutes: service.durationMinutes,
      priority: service.priority ?? "routine",
    })),
    escalationPhoneNumber: business.escalationPhoneNumber,
  };
}
