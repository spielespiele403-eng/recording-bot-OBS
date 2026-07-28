import type { Request, Response } from "express";
import { getByVoicePhoneNumber } from "../businesses/business.repository.js";
import { createCall } from "../calls/call.repository.js";
import { getPublicBookingLink } from "../calendar/calcom.service.js";
import { sendSms } from "./twilio.client.js";
import { logMissedCallSms } from "./smsLog.repository.js";

const MISSED_CALL_STATUSES = new Set(["no-answer", "busy", "failed"]);

export async function handleTwilioCallStatus(req: Request, res: Response) {
  const { To, From, CallStatus } = req.body as { To: string; From: string; CallStatus: string };

  if (!MISSED_CALL_STATUSES.has(CallStatus)) {
    res.status(200).json({ ok: true, ignored: true });
    return;
  }

  const business = await getByVoicePhoneNumber(To);
  if (!business) {
    res.status(404).json({ error: `No business found for number ${To}` });
    return;
  }

  const call = await createCall({
    businessId: business.id,
    fromNumber: From,
    toNumber: To,
    status: "MISSED",
  });

  const bookingLinkUrl = getPublicBookingLink(business);
  const body =
    `Hallo, hier ${business.name}. Wir konnten deinen Anruf gerade nicht entgegennehmen. ` +
    `Buche direkt einen Termin: ${bookingLinkUrl}`;

  try {
    const message = await sendSms({ to: From, from: business.twilioSmsFromNumber, body });
    await logMissedCallSms({
      businessId: business.id,
      callId: call.id,
      toNumber: From,
      twilioMessageSid: message.sid,
      bookingLinkUrl,
      status: "SENT",
    });
  } catch (error) {
    console.error("Failed to send missed-call recovery SMS", error);
    await logMissedCallSms({
      businessId: business.id,
      callId: call.id,
      toNumber: From,
      twilioMessageSid: "",
      bookingLinkUrl,
      status: "FAILED",
    });
  }

  res.status(200).json({ ok: true });
}
