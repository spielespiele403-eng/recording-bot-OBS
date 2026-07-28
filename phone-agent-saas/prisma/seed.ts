import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

// Placeholder demo business. vapiAssistantId / vapiPhoneNumberId / voicePhoneNumber
// are filled in for real once `npm run provision` has created the Vapi assistant
// and linked a phone number - see scripts/provisionBusiness.ts.
async function main() {
  const business = await prisma.business.upsert({
    where: { slug: "demo-handwerker" },
    update: {},
    create: {
      slug: "demo-handwerker",
      name: "Demo Handwerksbetrieb GmbH",
      industry: "handwerker",
      timezone: "Europe/Berlin",
      businessHours: JSON.stringify({
        mon: [{ start: "08:00", end: "17:00" }],
        tue: [{ start: "08:00", end: "17:00" }],
        wed: [{ start: "08:00", end: "17:00" }],
        thu: [{ start: "08:00", end: "17:00" }],
        fri: [{ start: "08:00", end: "15:00" }],
      }),
      escalationPhoneNumber: "+491700000000",
      faq: JSON.stringify([
        {
          question: "Bietet ihr Notdienst an?",
          answer: "Ja, bei Notfällen verbinden wir dich direkt mit einem Kollegen.",
        },
      ]),
      vapiAssistantId: "PENDING_PROVISIONING",
      vapiPhoneNumberId: "PENDING_PROVISIONING",
      voicePhoneNumber: "+490000000000",
      twilioSmsFromNumber: "+490000000000",
      calcomApiKey: "REPLACE_WITH_REAL_CALCOM_API_KEY",
      calcomUsername: "demo-handwerker",
      services: {
        create: [
          {
            name: "Kontrolltermin",
            durationMinutes: 30,
            calcomEventTypeId: 0,
            priority: "routine",
          },
          {
            name: "Notfall-Termin",
            durationMinutes: 60,
            calcomEventTypeId: 0,
            priority: "emergency",
          },
        ],
      },
    },
  });

  console.log(`Seeded business: ${business.name} (${business.id})`);
}

main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
