# Template 4: Lead Gen & Enrichment Engine

**Promise:** A steady supply of qualified, enriched, personalized prospects lands in your CRM or sequencer every week, without a human building lists.

**Buyer:** B2B agencies, SaaS sales teams, recruiters, and you. This is the same engine as your own outbound in [Step 3](../playbook/03-lead-generation.md).
**The number to sell on:** SDR hours spent on list building (often 40% of their week) × SDR cost.

## Flow

```
Input: ICP definition (industry, geo, size, titles, signals) in Airtable
  → Source: Apify (Google Maps / LinkedIn / job boards) or Apollo search
  → Dedupe against CRM + suppression list
  → Enrich: website scrape (homepage + about), email finder + verifier (e.g. MillionVerifier)
  → Claude: ICP fit score + 1-line personalized opener + pain hypothesis (JSON)
  → Filter: fit ≥ 7, email verified
  → Push to Instantly/Smartlead campaign with custom variables
  → Log to Airtable; weekly Slack summary (sourced / enriched / pushed)
```

## Stack

Make.com or n8n, Apify, Apollo, an email verifier, Claude API, Airtable, Instantly or Smartlead.

## Prompt skeleton

```
ICP: {{icp}}. Our offer: {{offer}}.
Company: {{company_name}} | Site text: {{website_text}} | Title: {{title}}
Return JSON only:
{"fit_score": 1-10, "reason": "...",
 "opener": "<1 sentence, specific to their site, no flattery clichés>",
 "pain_hypothesis": "..."}
```

## Intake questions

1. Who is your ICP? List 10 dream customers.
2. Which data sources and tools do you already pay for?
3. Target weekly volume.
4. Where should leads go (CRM, sequencer)?
5. What's on the suppression list (existing customers, competitors)?

## Add-ons

- Full cold email infrastructure setup (domains, inboxes, warmup): +$1,500
- Signal-based triggers (hiring, funding, new locations): +$1,000
- Reply classification and routing into the CRM: +$750

## Retainer hook

This is the easiest template to sell as a retainer. "Leads as a service" at $2–4K/month covers sourcing, list refreshes, copy testing, and deliverability monitoring.
