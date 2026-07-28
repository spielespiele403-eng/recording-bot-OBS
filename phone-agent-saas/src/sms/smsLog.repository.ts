import { prisma } from "../db/prisma.js";

export function logMissedCallSms(params: {
  businessId: string;
  callId: string;
  toNumber: string;
  twilioMessageSid: string;
  bookingLinkUrl: string;
  status: "SENT" | "FAILED";
}) {
  return prisma.missedCallSms.create({ data: params });
}
