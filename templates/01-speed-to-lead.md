# Template 1: Speed-to-Lead Responder

**Promise:** Every new lead gets a personalized text and email within 60 seconds, and hot leads get booked on the calendar automatically.

**Buyer:** Service businesses spending on ads (roofers, med spas, law firms, real estate, HVAC).
**The number to sell on:** Responding within 5 minutes rather than 30 raises qualification odds several times over. Ask what one closed job is worth, then ask how many leads go cold each month.

## Flow

```
Lead source (FB Lead Ads / website form / Google LSA / Zillow)
  → Webhook (Make)
  → Normalize fields (name, phone, email, service, source, message)
  → Dedupe against CRM
  → Claude: score lead 1–10 + classify service + draft first message (JSON)
  → Send SMS (Twilio) + email (Gmail/Outlook)
  → Create/Update CRM record (Airtable/HubSpot/GHL)
  → IF score ≥ 7 → Slack/SMS alert to owner + booking link
  → Follow-up sequence: +1h, +1d, +3d if no reply
  → Reply webhook → stop sequence, notify human
```

## Stack

Make.com, Twilio, Gmail/Outlook, Airtable (or the client's CRM), Claude API, Calendly/Cal.com.

## Airtable schema: `Leads`

| Field | Type |
| --- | --- |
| Name, Email, Phone | text / email / phone |
| Source | single select |
| Service | single select |
| Message | long text |
| Score | number (1–10) |
| Status | New, Contacted, Replied, Booked, Won, Lost |
| First Response At | date/time |
| Sequence Step | number |

## Prompt skeleton

```
You are the front desk for {{business_name}}, a {{business_type}} in {{city}}.
Lead: {{name}} | Service: {{service}} | Message: {{message}} | Source: {{source}}
Return JSON only:
{"score": 1-10, "service_category": "...", "urgency": "low|med|high",
 "sms": "<160 chars, friendly, includes {{booking_link}}>",
 "email_subject": "...", "email_body": "..."}
Scoring: +3 urgent language, +2 specific service, +2 budget/timeline mentioned, -3 spam/job seeker.
```

## Intake questions (custom 20%)

1. Where do leads come from now? Send a sample of each.
2. What CRM or tool do you use, and who should be alerted?
3. What services do you offer, and which ones are most valuable?
4. What are your business hours? What should happen with after-hours leads?
5. What's your booking link? What tone should we use, and are there phrases we should never say?

## Add-ons

- Missed-call text-back: +$500
- Reactivation campaign for old leads in the CRM: +$1,000
- Review request after a job is marked Won: +$500

## Retainer hook

Offer monthly prompt and copy tuning, a response-time report, new lead sources, and an A/B test of the first message.
