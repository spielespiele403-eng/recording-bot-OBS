import { Router } from "express";
import { verifyTwilioSignature } from "../middleware/verifyTwilioSignature.js";
import { handleTwilioCallStatus } from "./missedCall.controller.js";

export const missedCallRoutes = Router();

missedCallRoutes.post("/webhooks/twilio/call-status", verifyTwilioSignature, handleTwilioCallStatus);
