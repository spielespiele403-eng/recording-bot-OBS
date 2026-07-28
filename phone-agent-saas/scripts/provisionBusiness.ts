// Onboarding CLI: creates/updates the Vapi assistant for a Business row,
// imports its Twilio phone number into Vapi, and stores the resulting IDs.
// Usage: npm run provision -- <business-slug>
import { env } from "../src/config/env.js";
import { prisma } from "../src/db/prisma.js";
import { getBySlug } from "../src/businesses/business.repository.js";
import {
  createAssistantForBusiness,
  importTwilioNumber,
  updateAssistantForBusiness,
} from "../src/voice/vapi.client.js";

async function main() {
  const slug = process.argv[2] ?? "demo-handwerker";
  const business = await getBySlug(slug);

  if (!business) {
    throw new Error(`No business found with slug "${slug}" - seed it first via npm run prisma:seed`);
  }

  const webhookUrl = `${env.PUBLIC_BASE_URL}/webhooks/vapi`;
  const isFirstProvision = business.vapiAssistantId === "PENDING_PROVISIONING";

  const assistant = isFirstProvision
    ? await createAssistantForBusiness(business, webhookUrl)
    : await updateAssistantForBusiness(business, webhookUrl);

  console.log(`Vapi assistant ${isFirstProvision ? "created" : "updated"}: ${assistant.id}`);

  let vapiPhoneNumberId = business.vapiPhoneNumberId;
  let voicePhoneNumber = business.voicePhoneNumber;

  if (isFirstProvision) {
    const phoneNumber = await importTwilioNumber({
      twilioPhoneNumber: business.twilioSmsFromNumber,
      twilioAccountSid: env.TWILIO_ACCOUNT_SID,
      twilioAuthToken: env.TWILIO_AUTH_TOKEN,
      assistantId: assistant.id,
    });
    vapiPhoneNumberId = phoneNumber.id;
    voicePhoneNumber = business.twilioSmsFromNumber;
    console.log(`Twilio number imported into Vapi: ${phoneNumber.id} (${voicePhoneNumber})`);
  }

  await prisma.business.update({
    where: { id: business.id },
    data: {
      vapiAssistantId: assistant.id,
      vapiPhoneNumberId,
      voicePhoneNumber,
    },
  });

  console.log(`Business "${business.name}" provisioned successfully.`);
  console.log(`Configure Twilio's Status Callback for ${voicePhoneNumber} to: ${env.PUBLIC_BASE_URL}/webhooks/twilio/call-status`);
}

main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
