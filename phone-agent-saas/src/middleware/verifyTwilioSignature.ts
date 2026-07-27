import type { NextFunction, Request, Response } from "express";
import twilio from "twilio";
import { env } from "../config/env.js";

/** Verifies the X-Twilio-Signature header against the full callback URL + form
 * body, per Twilio's request-validation scheme. Requires PUBLIC_BASE_URL to
 * exactly match what Twilio was configured to call. */
export function verifyTwilioSignature(req: Request, res: Response, next: NextFunction) {
  const signature = req.header("x-twilio-signature");
  const fullUrl = `${env.PUBLIC_BASE_URL}${req.originalUrl}`;

  const isValid =
    !!signature &&
    twilio.validateRequest(env.TWILIO_AUTH_TOKEN, signature, fullUrl, req.body as Record<string, string>);

  if (!isValid) {
    res.status(401).json({ error: "Invalid Twilio signature" });
    return;
  }

  next();
}
