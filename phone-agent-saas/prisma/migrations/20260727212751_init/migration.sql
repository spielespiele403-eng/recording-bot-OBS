-- CreateTable
CREATE TABLE "Business" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "slug" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "industry" TEXT NOT NULL,
    "timezone" TEXT NOT NULL DEFAULT 'Europe/Berlin',
    "businessHours" TEXT NOT NULL,
    "escalationPhoneNumber" TEXT NOT NULL,
    "faq" TEXT,
    "vapiAssistantId" TEXT NOT NULL,
    "vapiPhoneNumberId" TEXT NOT NULL,
    "voicePhoneNumber" TEXT NOT NULL,
    "twilioSmsFromNumber" TEXT NOT NULL,
    "calcomApiKey" TEXT NOT NULL,
    "calcomUsername" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Service" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "businessId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "durationMinutes" INTEGER NOT NULL,
    "calcomEventTypeId" INTEGER NOT NULL,
    "priority" TEXT,
    CONSTRAINT "Service_businessId_fkey" FOREIGN KEY ("businessId") REFERENCES "Business" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Call" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "businessId" TEXT NOT NULL,
    "vapiCallId" TEXT,
    "fromNumber" TEXT NOT NULL,
    "toNumber" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'IN_PROGRESS',
    "transcript" TEXT,
    "summary" TEXT,
    "recordingUrl" TEXT,
    "startedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "endedAt" DATETIME,
    CONSTRAINT "Call_businessId_fkey" FOREIGN KEY ("businessId") REFERENCES "Business" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Appointment" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "businessId" TEXT NOT NULL,
    "callId" TEXT,
    "serviceId" TEXT NOT NULL,
    "calcomBookingId" TEXT NOT NULL,
    "customerName" TEXT NOT NULL,
    "customerPhone" TEXT NOT NULL,
    "startTime" DATETIME NOT NULL,
    "endTime" DATETIME NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'CONFIRMED',
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Appointment_businessId_fkey" FOREIGN KEY ("businessId") REFERENCES "Business" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Appointment_callId_fkey" FOREIGN KEY ("callId") REFERENCES "Call" ("id") ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT "Appointment_serviceId_fkey" FOREIGN KEY ("serviceId") REFERENCES "Service" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "MissedCallSms" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "businessId" TEXT NOT NULL,
    "callId" TEXT NOT NULL,
    "toNumber" TEXT NOT NULL,
    "twilioMessageSid" TEXT NOT NULL,
    "bookingLinkUrl" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "sentAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "MissedCallSms_businessId_fkey" FOREIGN KEY ("businessId") REFERENCES "Business" ("id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "MissedCallSms_callId_fkey" FOREIGN KEY ("callId") REFERENCES "Call" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Business_slug_key" ON "Business"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "Business_vapiAssistantId_key" ON "Business"("vapiAssistantId");

-- CreateIndex
CREATE UNIQUE INDEX "Business_vapiPhoneNumberId_key" ON "Business"("vapiPhoneNumberId");

-- CreateIndex
CREATE UNIQUE INDEX "Business_voicePhoneNumber_key" ON "Business"("voicePhoneNumber");

-- CreateIndex
CREATE INDEX "Service_businessId_idx" ON "Service"("businessId");

-- CreateIndex
CREATE UNIQUE INDEX "Call_vapiCallId_key" ON "Call"("vapiCallId");

-- CreateIndex
CREATE INDEX "Call_businessId_idx" ON "Call"("businessId");

-- CreateIndex
CREATE INDEX "Call_toNumber_idx" ON "Call"("toNumber");

-- CreateIndex
CREATE UNIQUE INDEX "Appointment_callId_key" ON "Appointment"("callId");

-- CreateIndex
CREATE UNIQUE INDEX "Appointment_calcomBookingId_key" ON "Appointment"("calcomBookingId");

-- CreateIndex
CREATE INDEX "Appointment_businessId_idx" ON "Appointment"("businessId");

-- CreateIndex
CREATE INDEX "MissedCallSms_businessId_idx" ON "MissedCallSms"("businessId");
