# Step 1: Learn the tools

> You don't need to be an expert. A couple dozen hours of YouTube courses gets you 80% of the way.
> The distance between you and an "automation specialist" is 50–100 hours of practice.

The goal here is to be **able to deliver the 5 templates**, not to know every feature.
Stop studying once you can build them. Anything you learn after that should come from client work.

## The stack (pick one per row, don't collect tools)

| Job | Default pick | Alternative |
| --- | --- | --- |
| Workflow automation | **Make.com** (easiest to sell and hand off) | n8n (self-hostable, cheaper at scale), Zapier |
| Database / CRM | **Airtable** | Google Sheets, ClickUp, HubSpot free |
| AI | **Claude API** (via HTTP module) | OpenAI |
| Forms | Tally | Typeform, Jotform |
| Scraping / enrichment | Apify | Apollo, Clay |
| Email sending | Instantly or Smartlead | Lemlist |
| Voice / phone | Vapi or Retell | Twilio |

## 60-hour curriculum

Each block ends with a **build**. If you skip the build, the hours don't count.

| Hours | Topic | Build (this is the proof) |
| --- | --- | --- |
| 0–8 | Make.com fundamentals: scenarios, modules, routers, filters, iterators, aggregators, error handlers | A form submission creates an Airtable record and sends a Slack/email notification |
| 8–14 | Airtable: tables, linked records, views, automations, interfaces | A mini CRM with Leads → Deals → Clients, linked records, and pipeline views |
| 14–20 | Webhooks and HTTP: JSON, auth headers, pagination, calling any API | Pull data from a public API into Airtable on a schedule |
| 20–30 | AI in workflows: prompting for structured JSON output, classification, extraction, summarization | An inbound email is classified by intent, gets a drafted reply, and is logged to Airtable |
| 30–38 | Scraping and enrichment: Apify actors, Google Maps and LinkedIn data, email finding | 200 local businesses in a niche, scraped, enriched, and loaded into a sheet |
| 38–46 | Documents: Google Docs/PDF generation from templates, e-signature | Fill out a form and get a generated proposal PDF by email |
| 46–54 | Voice / chat agents: Vapi or Retell basics, tool calls, calendar booking | An AI receptionist that answers FAQs and books appointments |
| 54–60 | Productizing: documentation, Loom walkthroughs, error alerting, client handoff | Package one build as a client-ready deliverable with an SOP and a Loom |

## YouTube search terms that work

- "Make.com full course beginner"
- "Airtable CRM tutorial"
- "Make.com HTTP module API tutorial"
- "AI automation agency build" (use this for the build ideas, and ignore the business-model hype)
- "Apify Google Maps scraper tutorial"
- "Vapi AI receptionist tutorial"

## Done criteria

You're done with Step 1 when:

- [ ] You've finished all 8 builds and have Looms of each.
- [ ] You can explain in one sentence what each build saves a business (hours or dollars).
- [ ] You've logged at least 50 hours in the dashboard's activity tracker.

Move on to Step 2 **immediately** after that. More courses are a low-ROI activity.
