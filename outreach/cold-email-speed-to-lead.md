# Cold outreach: Speed-to-Lead offer

A 3-email sequence for local service businesses that get inbound leads (roofers, HVAC, med spas, dentists,
law firms, real estate). It sells [Template 1](../templates/01-speed-to-lead.md).

Fill in the `{{variables}}` for each prospect. `{{personal_line}}` matters most: one specific, true sentence
about their business, such as their ads, reviews, website, or a recent job. [Template 4](../templates/04-lead-gen-engine.md) can generate it.

Plain text only. No links, images, or attachments in email 1.

---

## Email 1 (day 0)

**Subject:** `{{first_name}}, quick question about {{company}}`

```
Hi {{first_name}},

{{personal_line}}

Quick question: when a new lead comes in at 9pm, or while your team is out on a job,
how fast does someone get back to them?

For most {{niche}} businesses I talk to, it's a few hours. By then a lot of those
leads have already called the next company on Google.

I set up a simple system that texts and emails every new lead within 60 seconds,
answers their basic questions, and books the serious ones straight onto your calendar.
Nothing new for your team to learn.

Would it be useful if I recorded a 2-minute video showing how it would work for {{company}}?

{{your_name}}

P.S. Not the right person? Let me know who handles your leads and I'll reach out to them.
```

## Email 2 (day 3, reply in the same thread)

```
Hi {{first_name}},

Just to put a number on it: if {{company}} gets 50 leads a month and even 5 more of them
turn into jobs because someone replied in a minute instead of a few hours, that's
roughly {{5 × avg_job_value}} in extra revenue, from leads you're already paying for.

Happy to show you exactly how it would work. Want the video?

{{your_name}}
```

## Email 3 (day 7, reply in the same thread)

```
Hi {{first_name}},

I'll leave it here. If fast lead follow-up isn't a priority right now, no worries at all.

If it is, just reply "video" and I'll record a quick walkthrough for {{company}}.

{{your_name}}

Not interested? Reply "no" and I won't email again.
```

---

## When they reply

**Positive reply ("sure", "video", "how much?")**
```
Great. Here's the 2-min walkthrough of how it would work for {{company}}: {{loom_link}}

If it looks useful, grab a 15-min slot and I'll answer questions and scope it: {{booking_link}}
```

**"How much?"**
```
Setup is usually $1,500 one-time, depending on which tools you use. That covers the build,
testing, and 30 days of support. Most clients make it back with 1–2 extra jobs.

Easiest next step is a 15-min call so I can see your setup and give you an exact number: {{booking_link}}
```

**"Not interested" / "Remove me"**
Remove them from all campaigns immediately and add them to the suppression list. Don't reply.

## Sending rules

- Send from your outreach domains, **never** from your main domain (see [Step 3](../playbook/03-lead-generation.md)).
- Send at most 30–40 emails per inbox per day, after 14–21 days of warmup.
- Personalize `{{personal_line}}` for real. Generic flattery ("love your website!") kills reply rates.
- Legal: include your business name and physical mailing address in the signature (US CAN-SPAM), honor opt-outs
  right away, and check the rules for any country you email (for example, GDPR and CASL are stricter).
- Log every positive reply in the dashboard's Pipeline tab.
