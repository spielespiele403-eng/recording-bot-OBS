// SQLite has no native enum type, so Call.status is a plain string column in
// Prisma - this union is the single source of truth for valid values.
export type CallStatus =
  | "IN_PROGRESS"
  | "BOOKED"
  | "ESCALATED"
  | "MISSED"
  | "MISSED_RECOVERED"
  | "ABANDONED";
