# Template 3: Client Onboarding Autopilot

**Promise:** From "yes" to kickoff with zero manual admin: the contract, invoice, folders, project, welcome email, and kickoff booking all happen on their own.

**Buyer:** Agencies, consultants, coaches, accountants, and you. Run this on your own business first.
**The number to sell on:** 2–4 hours of admin per new client, plus a better first impression and faster cash collection.

## Flow

```
Trigger: CRM deal → "Closed Won" (or Tally intake form submitted)
  → Generate contract from Google Doc template → send via PandaDoc/DocuSign/Documenso
  → On signed webhook:
      → Create Stripe/QuickBooks invoice (deposit) → email payment link
  → On paid webhook:
      → Create Google Drive client folder from template structure
      → Create project in ClickUp/Asana/Notion from template (tasks + due dates)
      → Create Slack Connect channel / shared email thread
      → Send welcome email: next steps, intake form, kickoff booking link
      → Notify team in Slack
  → Intake form submitted → Claude summarizes into a kickoff brief doc
  → Reminders if contract unsigned (+2d) or invoice unpaid (+3d)
```

## Stack

Make.com, Google Docs/Drive, PandaDoc or Documenso, Stripe, ClickUp/Asana/Notion, Slack, Tally, Claude API.

## Intake questions

1. Walk me through what happens today after a client says yes, step by step.
2. Contract template, invoice terms, and deposit percentage.
3. Folder structure and project task template.
4. Welcome email copy and kickoff call link.
5. Who needs to be notified at each stage?

## Add-ons

- Offboarding flow with review and referral request: +$750
- Monthly client reporting automation: +$1,500
- Client portal (Softr on top of Airtable): +$2,000

## Retainer hook

Offer to automate the next process in line: delivery, reporting, or invoicing. Onboarding is the way in to a full operations retainer.
