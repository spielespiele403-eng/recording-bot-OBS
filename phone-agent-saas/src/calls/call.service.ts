import { prisma } from "../db/prisma.js";
import { getByVapiCallId, updateCallStatus } from "./call.repository.js";

export async function logCallOutcome(vapiCallId: string, status: "BOOKED" | "ESCALATED") {
  const call = await getByVapiCallId(vapiCallId);
  if (!call) {
    throw new Error(`No Call row found for vapiCallId=${vapiCallId}`);
  }
  return updateCallStatus(call.id, status);
}

export function getOrCreateInProgressCall(params: {
  businessId: string;
  vapiCallId: string;
  fromNumber: string;
  toNumber: string;
}) {
  return prisma.call.upsert({
    where: { vapiCallId: params.vapiCallId },
    update: {},
    create: {
      businessId: params.businessId,
      vapiCallId: params.vapiCallId,
      fromNumber: params.fromNumber,
      toNumber: params.toNumber,
      status: "IN_PROGRESS",
    },
  });
}
