import type { Request, Response } from "express";
import { getByVapiAssistantId } from "../businesses/business.repository.js";
import { getOrCreateInProgressCall } from "../calls/call.service.js";
import { finalizeCall } from "../calls/call.repository.js";
import { dispatchToolCall } from "./tools/toolDispatcher.js";
import type { VapiWebhookPayload } from "../types/vapi.types.js";

export async function handleVapiWebhook(req: Request, res: Response) {
  const { message } = req.body as VapiWebhookPayload;

  if (message.type === "tool-calls" && message.toolCalls && message.call) {
    const call = message.call;
    const business = await getByVapiAssistantId(call.assistantId);
    if (!business) {
      res.status(404).json({ error: `No business found for assistantId=${call.assistantId}` });
      return;
    }

    const dbCall = await getOrCreateInProgressCall({
      businessId: business.id,
      vapiCallId: call.id,
      fromNumber: call.customer?.number ?? "unknown",
      toNumber: business.voicePhoneNumber,
    });

    const results = await Promise.all(
      message.toolCalls.map((toolCall) =>
        dispatchToolCall(toolCall, business, { vapiCallId: call.id, callId: dbCall.id }),
      ),
    );

    res.json({ results });
    return;
  }

  if (message.type === "end-of-call-report" && message.call) {
    await finalizeCall(message.call.id, {
      transcript: message.transcript,
      summary: message.summary,
      recordingUrl: message.recordingUrl,
      fallbackStatus: "ABANDONED",
    });
    res.status(200).json({ ok: true });
    return;
  }

  // Other message types (status-update, transcript, etc.) - just acknowledge.
  res.status(200).json({ ok: true });
}
