import { Router } from "express";
import { getBySlug, listBusinesses } from "./business.repository.js";
import { getBusinessContext } from "./business.service.js";

export const businessRoutes = Router();

// Config-via-API for v1 (no admin UI yet) - lets an operator inspect what a
// business is currently configured with, across any industry.
businessRoutes.get("/api/businesses", async (_req, res) => {
  const businesses = await listBusinesses();
  res.json(businesses.map((business) => getBusinessContext(business)));
});

businessRoutes.get("/api/businesses/:slug", async (req, res) => {
  const business = await getBySlug(req.params.slug);
  if (!business) {
    res.status(404).json({ error: "Business not found" });
    return;
  }
  res.json(getBusinessContext(business));
});
