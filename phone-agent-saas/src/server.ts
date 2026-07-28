import express from "express";
import { env } from "./config/env.js";
import { businessRoutes } from "./businesses/business.routes.js";
import { vapiWebhookRoutes } from "./voice/vapi.webhook.routes.js";
import { missedCallRoutes } from "./sms/missedCall.routes.js";
import { errorHandler } from "./middleware/errorHandler.js";

const app = express();

app.use(express.json());
// Twilio webhooks POST application/x-www-form-urlencoded - needed for signature
// verification (twilio.validateRequest expects the parsed form params).
app.use(express.urlencoded({ extended: false }));

app.get("/health", (_req, res) => res.json({ ok: true }));

app.use(businessRoutes);
app.use(vapiWebhookRoutes);
app.use(missedCallRoutes);

app.use(errorHandler);

app.listen(env.PORT, () => {
  console.log(`phone-agent-saas listening on port ${env.PORT}`);
});
