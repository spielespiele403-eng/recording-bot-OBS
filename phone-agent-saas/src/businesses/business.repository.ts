import { prisma } from "../db/prisma.js";

export function getBySlug(slug: string) {
  return prisma.business.findUnique({
    where: { slug },
    include: { services: true },
  });
}

export function getByVapiAssistantId(vapiAssistantId: string) {
  return prisma.business.findUnique({
    where: { vapiAssistantId },
    include: { services: true },
  });
}

export function getByVoicePhoneNumber(voicePhoneNumber: string) {
  return prisma.business.findUnique({
    where: { voicePhoneNumber },
    include: { services: true },
  });
}

export function listBusinesses() {
  return prisma.business.findMany({ include: { services: true } });
}
