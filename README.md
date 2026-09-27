# Goaldenway

The operating system for getting an automation services business to **$25,000/month**.

Built from the 5-step roadmap:

1. **Learn the tools**: 50–100 hours of focused practice, not mastery.
2. **Create 5 templates**: repeatable systems that do 80% of the job; customize the last 20% per client.
3. **Generate leads**: cold email, communities, and Upwork/Fiverr, all running at the same time.
4. **Retain and ascend**: turn $1K one-off projects into $50K+/year relationships.
5. **Repeat**: reinvest the first dollars to bootstrap everything else.

The rule behind all of it: **only do activities that correlate with revenue.**

## What's in this repo

| Path | What it is |
| --- | --- |
| [`playbook/01-learn-the-tools.md`](playbook/01-learn-the-tools.md) | A 60-hour curriculum with the exact build exercises to do |
| [`playbook/02-templates.md`](playbook/02-templates.md) | How templates work: the 80/20 rule, pricing, and delivery |
| [`templates/`](templates/) | The 5 productized templates, each with its own build spec |
| [`playbook/03-lead-generation.md`](playbook/03-lead-generation.md) | Cold email infrastructure, sequences, Upwork/Fiverr, and communities |
| [`outreach/cold-email-speed-to-lead.md`](outreach/cold-email-speed-to-lead.md) | A ready-to-send 3-email cold sequence, reply scripts, and sending rules |
| [`playbook/04-retain-and-ascend.md`](playbook/04-retain-and-ascend.md) | The package ladder, retainers, and upsell scripts |
| [`playbook/05-repeat-operating-cadence.md`](playbook/05-repeat-operating-cadence.md) | Weekly scorecard, the VA SOP, and reinvestment rules |
| [`dashboard/index.html`](dashboard/index.html) | A single-file tracker for pipeline, clients, MRR, and your gap to $25K |

## The $25K math

$25K/month comes from stacking retainers on top of project revenue. One way to get there:

| Revenue line | Count | Price | Monthly |
| --- | --- | --- | --- |
| Retainers (Growth tier) | 6 | $2,000/mo | $12,000 |
| Retainers (Scale tier) | 2 | $3,500/mo | $7,000 |
| New builds (Starter/System) | 2 | $3,000 avg | $6,000 |
| **Total** | | | **$25,000** |

That means about **8 retained clients** plus **2 new builds a month**. At a 20% close rate on sales calls,
that's about 10 calls a month. If 1% of cold emails turn into a booked call, cold email alone needs about
1,000 sends a month (about 250 a week). Upwork and communities cut that number.
The dashboard recalculates these numbers from your real conversion rates.

## Milestones

| Stage | Monthly revenue | Unlock |
| --- | --- | --- |
| 0 → 1 | First $1K | Hire nothing. Reinvest in email infrastructure (domains and inboxes). |
| 1 → 5 | $5K | Hire a part-time VA for lead research and inbox management. |
| 5 → 15 | $15K | Move every new client onto a retainer. Raise Starter prices. |
| 15 → 25 | $25K | Standardize delivery with the templates. The VA handles onboarding. |

## Using the dashboard

Open `dashboard/index.html` in a browser. It doesn't need a build step or a server. Your data is saved in the browser's
`localStorage`. Use **Export** and **Import** to back it up or move it between machines. You can also deploy
the `dashboard/` folder as a static site on Netlify or GitHub Pages.
