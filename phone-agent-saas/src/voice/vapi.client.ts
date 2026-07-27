import { VapiClient, type Vapi } from "@vapi-ai/server-sdk";
import { env } from "../config/env.js";
import type { BusinessWithServices } from "../businesses/business.service.js";
import { getBusinessContext } from "../businesses/business.service.js";

const vapi = new VapiClient({ token: env.VAPI_API_KEY });

// Vapi's Server config has no built-in "secret" field - the shared secret is
// carried as a custom header instead, checked by verifyVapiSignature.
const WEBHOOK_SECRET_HEADER = "x-webhook-secret";

const TOOL_DEFINITIONS: Vapi.AnthropicModelToolsItem[] = [
  {
    type: "function" as const,
    function: {
      name: "get_business_info",
      description: "Returns the business's opening hours, services and FAQ answers.",
      parameters: { type: "object" as const, properties: {} },
    },
  },
  {
    type: "function" as const,
    function: {
      name: "check_availability",
      description: "Checks available appointment slots for a given service and date range.",
      parameters: {
        type: "object" as const,
        properties: {
          serviceName: { type: "string" },
          startDate: { type: "string", description: "ISO date, e.g. 2026-08-01" },
          endDate: { type: "string", description: "ISO date, e.g. 2026-08-07" },
        },
        required: ["serviceName", "startDate", "endDate"],
      },
    },
  },
  {
    type: "function" as const,
    function: {
      name: "book_appointment",
      description: "Books an appointment for the caller at a specific available slot.",
      parameters: {
        type: "object" as const,
        properties: {
          serviceName: { type: "string" },
          slotStart: { type: "string", description: "ISO datetime of the chosen slot" },
          customerName: { type: "string" },
          customerPhone: { type: "string" },
        },
        required: ["serviceName", "slotStart", "customerName", "customerPhone"],
      },
    },
  },
];

function buildSystemPrompt(business: BusinessWithServices): string {
  const context = getBusinessContext(business);
  return [
    `Du bist der Telefonassistent von "${context.name}" (Branche: ${context.industry}).`,
    `Öffnungszeiten (JSON): ${JSON.stringify(context.businessHours)}`,
    `Angebotene Leistungen (JSON): ${JSON.stringify(context.services)}`,
    context.faq.length > 0 ? `Häufige Fragen (JSON): ${JSON.stringify(context.faq)}` : "",
    "Beantworte Fragen freundlich und kurz auf Deutsch. Nutze get_business_info für Öffnungszeiten/Leistungen/FAQ.",
    "Wenn der Anrufer einen Termin möchte, nutze check_availability und danach book_appointment.",
    `Bei Notfällen oder wenn du nicht weiterhelfen kannst, biete an, an ${context.escalationPhoneNumber} weiterzuleiten.`,
  ]
    .filter(Boolean)
    .join("\n");
}

export async function createAssistantForBusiness(business: BusinessWithServices, webhookUrl: string) {
  return vapi.assistants.create({
    name: business.name,
    model: {
      provider: "anthropic",
      model: "claude-sonnet-4-6",
      messages: [{ role: "system", content: buildSystemPrompt(business) }],
      tools: TOOL_DEFINITIONS,
    },
    server: { url: webhookUrl, headers: { [WEBHOOK_SECRET_HEADER]: env.VAPI_WEBHOOK_SECRET } },
  });
}

export async function updateAssistantForBusiness(business: BusinessWithServices, webhookUrl: string) {
  return vapi.assistants.update({
    id: business.vapiAssistantId,
    name: business.name,
    model: {
      provider: "anthropic",
      model: "claude-sonnet-4-6",
      messages: [{ role: "system", content: buildSystemPrompt(business) }],
      tools: TOOL_DEFINITIONS,
    },
    server: { url: webhookUrl, headers: { [WEBHOOK_SECRET_HEADER]: env.VAPI_WEBHOOK_SECRET } },
  });
}

export async function importTwilioNumber(params: {
  twilioPhoneNumber: string;
  twilioAccountSid: string;
  twilioAuthToken: string;
  assistantId: string;
}) {
  return vapi.phoneNumbers.create({
    provider: "twilio",
    number: params.twilioPhoneNumber,
    twilioAccountSid: params.twilioAccountSid,
    twilioAuthToken: params.twilioAuthToken,
    assistantId: params.assistantId,
  });
}
