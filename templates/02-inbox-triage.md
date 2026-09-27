# Template 2: AI Inbox & Support Triage

**Promise:** Every inbound email is labeled, prioritized, and has a draft reply waiting, and the routine ones get answered automatically.

**Buyer:** E-commerce brands, SaaS, agencies, anyone with a shared support@ or info@ inbox.
**The number to sell on:** Hours per day spent in the inbox × hourly cost. A typical result is a 60–80% cut in handling time.

## Flow

```
New email (Gmail/Outlook watch) or helpdesk webhook (Gorgias/Zendesk/Help Scout)
  → Strip signatures/quoted text
  → Lookup customer (Shopify/Stripe/CRM) for context: orders, plan, LTV
  → Claude: classify intent + priority + sentiment + extract entities (order #, etc.)
  → Router:
      • Routine (order status, FAQ, refund policy) → draft reply → auto-send if confidence ≥ 0.9, else save as draft
      • Sales lead → forward to sales + create CRM deal
      • Urgent / angry / VIP → Slack alert, tag, no auto-send
      • Spam/vendor → archive
  → Apply labels, log to Airtable for reporting
```

## Stack

Make.com, Gmail/Outlook or a helpdesk, Shopify/Stripe lookup, Claude API, Airtable, Slack.

## Prompt skeleton

```
Classify this email for {{company}}. Knowledge base: {{kb}}. Customer context: {{customer}}.
Return JSON only:
{"intent": "order_status|refund|product_question|sales|complaint|partnership|spam|other",
 "priority": "low|normal|high|urgent", "sentiment": -1..1, "confidence": 0..1,
 "entities": {"order_number": null}, "reply": "<draft in brand voice, or null>"}
Never promise refunds beyond policy. If unsure, set confidence < 0.6.
```

## Intake questions

1. Which inboxes or helpdesk do you use? Roughly how many emails a day?
2. Export your 50 most common questions and your best replies to them.
3. Refund, shipping, and returns policies.
4. Who handles escalations? What counts as VIP?
5. What's your auto-send risk tolerance: draft everything, or auto-send the routine ones?

## Add-ons

- Weekly insights report (top issues, sentiment trend): +$500
- Chat widget using the same knowledge base: +$1,500
- Multilingual replies: +$500

## Retainer hook

Offer to grow the knowledge base, tune accuracy (track the auto-send rate as the KPI), and add new intents as the product changes.
