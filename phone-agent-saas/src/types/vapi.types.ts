// Minimal shapes for the subset of Vapi's server-webhook payloads this project
// handles. Kept as one flat, mostly-optional interface (rather than a strict
// discriminated union) since Vapi sends many message types we don't act on -
// callers must check `type` and the presence of the fields they need.

export interface VapiCallRef {
  id: string;
  assistantId: string;
  customer?: { number?: string };
  phoneNumberId?: string;
}

export interface VapiToolCall {
  id: string;
  type: "function";
  function: {
    name: string;
    arguments: Record<string, unknown>;
  };
}

export interface VapiServerMessage {
  type: string;
  call?: VapiCallRef;
  toolCalls?: VapiToolCall[];
  transcript?: string;
  summary?: string;
  recordingUrl?: string;
  endedReason?: string;
}

export interface VapiWebhookPayload {
  message: VapiServerMessage;
}

export interface VapiToolResult {
  toolCallId: string;
  result: string;
}
