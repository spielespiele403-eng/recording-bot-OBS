import type { NextFunction, Request, Response } from "express";
import { env } from "../config/env.js";

/** Vapi's Server config has no built-in signing scheme - instead we configure
 * a shared secret as a custom header (`x-webhook-secret`) on the assistant's
 * server config (see src/voice/vapi.client.ts) and check it here. */
export function verifyVapiSignature(req: Request, res: Response, next: NextFunction) {
  const receivedSecret = req.header("x-webhook-secret");

  if (!receivedSecret || receivedSecret !== env.VAPI_WEBHOOK_SECRET) {
    res.status(401).json({ error: "Invalid Vapi webhook secret" });
    return;
  }

  next();
}
