import { prisma } from "../db/prisma.js";

export function createAppointment(params: {
  businessId: string;
  callId?: string;
  serviceId: string;
  calcomBookingId: string;
  customerName: string;
  customerPhone: string;
  startTime: Date;
  endTime: Date;
}) {
  return prisma.appointment.create({ data: params });
}
