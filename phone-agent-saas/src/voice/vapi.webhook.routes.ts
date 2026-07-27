import { Router } from "express";
import { verifyVapiSignature } from "../middleware/verifyVapiSignature.js";
import { handleVapiWebhook } from "./vapi.webhook.controller.js";

export const vapiWebhookRoutes = Router();

vapiWebhookRoutes.post("/webhooks/vapi", verifyVapiSignature, handleVapiWebhook);
