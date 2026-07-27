import { prisma } from "../db/prisma.js";
import type { CallStatus } from "./call.types.js";

export function createCall(params: {
  businessId: string;
  vapiCallId?: string;
  fromNumber: string;
  toNumber: string;
  status?: CallStatus;
}) {
  return prisma.call.create({
    data: {
      businessId: params.businessId,
      vapiCallId: params.vapiCallId,
      fromNumber: params.fromNumber,
      toNumber: params.toNumber,
      status: params.status ?? "IN_PROGRESS",
    },
  });
}

export function getByVapiCallId(vapiCallId: string) {
  return prisma.call.findUnique({ where: { vapiCallId } });
}

export function updateCallStatus(callId: string, status: CallStatus) {
  return prisma.call.update({
    where: { id: callId },
    data: { status },
  });
}

export function finalizeCall(
  vapiCallId: string,
  params: { transcript?: string; summary?: string; recordingUrl?: string; fallbackStatus: CallStatus },
) {
  return prisma.call.updateMany({
    where: { vapiCallId, status: "IN_PROGRESS" },
    data: {
      transcript: params.transcript,
      summary: params.summary,
      recordingUrl: params.recordingUrl,
      status: params.fallbackStatus,
      endedAt: new Date(),
    },
  });
}

export function listCallsForBusiness(businessId: string) {
  return prisma.call.findMany({
    where: { businessId },
    orderBy: { startedAt: "desc" },
    include: { appointment: true },
  });
}
