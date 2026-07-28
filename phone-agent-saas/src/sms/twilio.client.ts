import twilio from "twilio";
import { env } from "../config/env.js";

const client = twilio(env.TWILIO_ACCOUNT_SID, env.TWILIO_AUTH_TOKEN);

export async function sendSms(params: { to: string; from: string; body: string }) {
  return client.messages.create({
    to: params.to,
    from: params.from,
    body: params.body,
  });
}
