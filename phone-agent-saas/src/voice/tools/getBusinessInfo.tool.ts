import type { BusinessWithServices } from "../../businesses/business.service.js";
import { getBusinessContext } from "../../businesses/business.service.js";

export function getBusinessInfo(business: BusinessWithServices): string {
  return JSON.stringify(getBusinessContext(business));
}
