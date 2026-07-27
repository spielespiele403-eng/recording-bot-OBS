import type { VapiToolCall, VapiToolResult } from "../../types/vapi.types.js";
import type { BusinessWithServices } from "../../businesses/business.service.js";
import { getBusinessInfo } from "./getBusinessInfo.tool.js";
import { checkAvailability } from "./checkAvailability.tool.js";
import { bookAppointment } from "./bookAppointment.tool.js";

export async function dispatchToolCall(
  toolCall: VapiToolCall,
  business: BusinessWithServices,
  context: { vapiCallId: string; callId: string },
): Promise<VapiToolResult> {
  const { name, arguments: args } = toolCall.function;

  let result: string;
  switch (name) {
    case "get_business_info":
      result = getBusinessInfo(business);
      break;
    case "check_availability":
      result = await checkAvailability(business, args as { serviceName: string; startDate: string; endDate: string });
      break;
    case "book_appointment":
      result = await bookAppointment(
        business,
        args as { serviceName: string; slotStart: string; customerName: string; customerPhone: string },
        context,
      );
      break;
    default:
      result = JSON.stringify({ error: `Unknown tool "${name}"` });
  }

  return { toolCallId: toolCall.id, result };
}
