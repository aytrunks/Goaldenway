#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic();

async function generateCaptions(editPlanPath) {
  if (!fs.existsSync(editPlanPath)) {
    console.error(`❌ Edit plan not found: ${editPlanPath}`);
    process.exit(1);
  }

  const plan = JSON.parse(fs.readFileSync(editPlanPath, 'utf8'));
  const videoPath = plan.videoPath;

  console.log(`\n🎬 Generating captions for: ${path.basename(videoPath)}`);
  console.log(`📐 Structure detected: ${plan.editInstructions.structure}\n`);

  const captions = {
    hook: plan.editInstructions.hook,
    formats: {}
  };

  // Generate captions for each format
  const formats = [
    {
      name: 'longForm',
      label: 'Long-form (1:00–1:35)',
      instruction: 'Full detailed process from start to finish. Hook + explanation of steps + before/after reveal + CTA. Natural, conversational tone.'
    },
    {
      name: 'shortForm',
      label: 'Short-form (7–18s)',
      instruction: 'Quick hook opening + quick before/after reveal + CTA. Punchy, fast-paced. Must be scannable in 15 seconds.'
    },
    {
      name: 'carousel',
      label: 'Carousel (3-5 slides)',
      instruction: 'One short caption per slide. Slide 1: Hook/Problem. Slide 2-4: Process/Reveal. Slide 5: CTA. Each 1-2 sentences.'
    }
  ];

  for (const format of formats) {
    console.log(`✍️  Generating ${format.label}...`);

    try {
      const response = await client.messages.create({
        model: "claude-3-5-sonnet-20241022",
        max_tokens: 400,
        messages: [
          {
            role: "user",
            content: `You're writing social media captions for boat detailing content. Use this hook and context:

Hook: "${plan.editInstructions.hook}"

Video type: ${plan.editInstructions.structure}
Format: ${format.label}
Requirements: ${format.instruction}

Generate the caption. Include the hook, description of the boat transformation, and end with "The Boat House Cape Coral. 📍 DM me" as the CTA.

Write ONLY the caption text, no explanations.`
          }
        ]
      });

      const caption = response.content[0].text.trim();
      captions.formats[format.name] = {
        label: format.label,
        text: caption
      };

      console.log(`  ✅ ${format.label}:`);
      console.log(`     "${caption.substring(0, 80)}..."\n`);

    } catch (err) {
      console.error(`  ❌ Failed: ${err.message}`);
    }
  }

  // Save captions
  const captionsPath = editPlanPath.replace('_edit-plan.json', '_captions.json');
  fs.writeFileSync(captionsPath, JSON.stringify(captions, null, 2));
  console.log(`\n✅ Captions saved: ${path.basename(captionsPath)}`);

  return captions;
}

async function main() {
  const editPlanPath = process.argv[2];

  if (!editPlanPath) {
    console.log(`Usage: node video-caption-generator.js <edit-plan-json>`);
    console.log(`\nExample: node video-caption-generator.js boat-detail_edit-plan.json`);
    console.log(`\nRun after: node video-analyzer.js <video-file>`);
    process.exit(1);
  }

  try {
    await generateCaptions(editPlanPath);
    console.log(`\n📋 Next: Copy captions to your video editor and social posts`);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
