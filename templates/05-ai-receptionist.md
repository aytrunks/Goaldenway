# Template 5: AI Voice Receptionist

**Promise:** Every call gets answered 24/7. FAQs get handled, appointments get booked, and the details land in the CRM.

**Buyer:** Dental and medical clinics, home services, salons, law firms, restaurants.
**The number to sell on:** Missed calls per week × close rate × average job value. Most local businesses miss 20–40% of their calls.

## Flow

```
Inbound call → forwarded number (Twilio) → Vapi/Retell agent
  Agent tools (via Make webhooks):
    • check_availability(date) → Google Calendar / booking system
    • book_appointment(name, phone, service, time)
    • lookup_faq(question) → knowledge base
    • transfer_to_human() during business hours if requested/urgent
  → End-of-call webhook: transcript + summary + outcome
  → Claude: extract structured data (JSON) → CRM record
  → SMS confirmation to caller; Slack/email summary to owner
  → Daily digest: calls, bookings, missed opportunities
```

## Stack

Vapi or Retell, Twilio, Make.com, Google Calendar (or Acuity/Jane/ServiceTitan), Airtable/CRM, Claude API.

## Pricing

This is a setup fee plus a monthly platform fee. Voice minutes are a recurring cost, which makes this template **retainer-native**.
Charge $2,500 for setup plus $500–1,000/month, covering minutes, monitoring, and tuning.

## Intake questions

1. Call volume, peak hours, and the current missed-call rate.
2. Services, prices, and the top 30 FAQs.
3. Booking system and appointment rules (durations, buffers, staff).
4. When should the agent transfer the call, and to whom?
5. Voice, name, and greeting. Any compliance constraints (for example HIPAA)?

## Add-ons

- Outbound reminder and no-show calls: +$1,000
- Multilingual agent: +$500
- Post-visit review request calls or texts: +$500

## Retainer hook

The retainer is built in: monthly transcript review, FAQ updates, and a conversion report.
