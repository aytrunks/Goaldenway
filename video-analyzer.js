#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic();

// Pre-loaded hooks for captions
const HOOKS = [
  "Neglect costs money. This boat sat for months, which means oxidation, mold, saltwater damage. One detail later? Ready to sell or rent. That's preservation.",
  "Your boat's value drops 10% per month of neglect. Cleaning and detailing isn't vanity — it's protecting your investment.",
  "I restore boats better than I restore my life choices.",
  "Your boat's been judging you the whole time.",
  "This is technically an ad. Your boat is technically a health hazard. Let's fix the more urgent one.",
  "I clean boats for a living and still can't parallel park mine. Nobody's perfect. Yours can be, though.",
  "There's a version of your boat that looks incredible in golden hour light. It's currently buried under three months of neglect.",
  "Your hull has more baggage than my last relationship, and that one ended over a group chat.",
  "Neglected boats lose value fast. Statistic. I should mention I have zero peer-reviewed studies. The boat thing's still true."
];

async function extractFrames(videoPath, outputDir, interval = 5) {
  console.log(`📹 Extracting frames from ${path.basename(videoPath)} (every ${interval}s)...`);

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  try {
    execSync(`ffmpeg -i "${videoPath}" -vf fps=1/${interval} "${outputDir}/frame_%04d.png" -hide_banner -loglevel error`, {
      stdio: 'pipe'
    });

    const frames = fs.readdirSync(outputDir).filter(f => f.endsWith('.png')).sort();
    console.log(`✅ Extracted ${frames.length} frames`);
    return frames;
  } catch (err) {
    console.error('❌ ffmpeg error. Install with: brew install ffmpeg (Mac) or apt install ffmpeg (Linux)');
    process.exit(1);
  }
}

async function analyzeFrames(frames, outputDir) {
  console.log(`\n🤖 Analyzing frames with Claude...`);

  const analysis = {
    totalFrames: frames.length,
    keyMoments: [],
    beforeAfterPoints: [],
    structure: null,
    recommendations: []
  };

  // Analyze every Nth frame to save API calls
  const framesToAnalyze = frames.filter((_, i) => i % Math.ceil(frames.length / 10) === 0);
  console.log(`📊 Analyzing ${framesToAnalyze.length} key frames (sampling)...`);

  for (let i = 0; i < framesToAnalyze.length; i++) {
    const frame = framesToAnalyze[i];
    const frameNum = frames.indexOf(frame);
    const timestamp = frameNum * 5; // assuming 5s interval

    const framePath = path.join(outputDir, frame);
    const imageData = fs.readFileSync(framePath);
    const base64 = imageData.toString('base64');

    try {
      const response = await client.messages.create({
        model: "claude-3-5-sonnet-20241022",
        max_tokens: 300,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "image",
                source: {
                  type: "base64",
                  media_type: "image/png",
                  data: base64
                }
              },
              {
                type: "text",
                text: "Analyze this frame from a boat detailing video. Identify: 1) Is this BEFORE (dirty/neglected) or AFTER (clean/detailed) state? 2) What's happening (spraying water, scrubbing, detail work, rinsing, finished product)? 3) How important is this moment (1-10) for a short-form social video? Keep response brief."
              }
            ]
          }
        ]
      });

      const analysis_text = response.content[0].text;

      const isBefore = analysis_text.toLowerCase().includes('before');
      const isAfter = analysis_text.toLowerCase().includes('after');
      const importance = analysis_text.match(/\d/) ? parseInt(analysis_text.match(/\d/)[0]) : 5;

      if (isBefore || isAfter) {
        analysis.beforeAfterPoints.push({
          frameNum,
          timestamp: `${Math.floor(timestamp / 60)}:${String(timestamp % 60).padStart(2, '0')}`,
          state: isBefore ? 'BEFORE' : 'AFTER',
          description: analysis_text.substring(0, 100)
        });
      }

      if (importance >= 7) {
        analysis.keyMoments.push({
          frameNum,
          timestamp: `${Math.floor(timestamp / 60)}:${String(timestamp % 60).padStart(2, '0')}`,
          importance,
          description: analysis_text.substring(0, 80)
        });
      }

      console.log(`  Frame ${frameNum}: ${analysis_text.substring(0, 60)}...`);
    } catch (err) {
      console.error(`  ⚠️  Frame ${frameNum} analysis failed: ${err.message}`);
    }
  }

  return analysis;
}

function generateEditPlan(analysis, videoPath) {
  console.log(`\n✂️ Generating edit plan...`);

  const randomHook = HOOKS[Math.floor(Math.random() * HOOKS.length)];

  // Detect structure
  let structure = "Generic";
  if (analysis.beforeAfterPoints.length >= 2) {
    const beforeCount = analysis.beforeAfterPoints.filter(p => p.state === 'BEFORE').length;
    const afterCount = analysis.beforeAfterPoints.filter(p => p.state === 'AFTER').length;

    if (beforeCount > 0 && afterCount > 0) {
      structure = "Before/After Reveal";
    } else if (beforeCount > afterCount) {
      structure = "Problem Setup";
    } else {
      structure = "Solution Showcase";
    }
  }

  analysis.structure = structure;

  // Generate edit recommendations
  const sortedMoments = analysis.keyMoments.sort((a, b) => b.importance - a.importance);

  if (sortedMoments.length > 0) {
    analysis.recommendations.push("📌 Hero moment: " + sortedMoments[0].timestamp);
  }

  if (analysis.beforeAfterPoints.length >= 2) {
    const beforeMoments = analysis.beforeAfterPoints.filter(p => p.state === 'BEFORE');
    const afterMoments = analysis.beforeAfterPoints.filter(p => p.state === 'AFTER');
    if (beforeMoments.length > 0 && afterMoments.length > 0) {
      analysis.recommendations.push(`🎬 Cut from ${beforeMoments[0].timestamp} to ${afterMoments[0].timestamp} for reveal`);
    }
  }

  analysis.recommendations.push(`💬 Caption: "${randomHook}"`);
  analysis.recommendations.push(`📍 Add: "The Boat House Cape Coral. DM me"`);

  return analysis;
}

function outputEditManifest(analysis, videoPath, outputPath) {
  const manifest = {
    video: path.basename(videoPath),
    videoPath: videoPath,
    generatedAt: new Date().toISOString(),
    analysis: analysis,
    editInstructions: {
      format: {
        longForm: "1:00–1:35 — full before to after process",
        shortForm: "7–18s — quick before/after cut",
        carousel: "3-5 key frames, 2-3s each"
      },
      hook: HOOKS[Math.floor(Math.random() * HOOKS.length)],
      cta: "DM me",
      structure: analysis.structure,
      keyFrames: analysis.keyMoments.slice(0, 5),
      beforeAfterPoints: analysis.beforeAfterPoints,
      recommendations: analysis.recommendations
    },
    importInstructions: {
      capcut: "Copy key frame timestamps into CapCut as cut points",
      premiere: "Import this JSON and use timestamps to mark in/out points",
      davinci: "Use DaVinci Resolve markers at provided timestamps"
    }
  };

  fs.writeFileSync(outputPath, JSON.stringify(manifest, null, 2));
  console.log(`\n✅ Edit plan saved: ${outputPath}`);

  return manifest;
}

function printReport(analysis) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`📊 EDIT PLAN SUMMARY`);
  console.log(`${'='.repeat(60)}`);
  console.log(`\n📹 Video Structure: ${analysis.structure}`);
  console.log(`\n🔑 Key Moments Found: ${analysis.keyMoments.length}`);
  analysis.keyMoments.slice(0, 3).forEach((m, i) => {
    console.log(`  ${i + 1}. [${m.timestamp}] Importance: ${m.importance}/10`);
  });

  console.log(`\n🔄 Before/After Transitions: ${analysis.beforeAfterPoints.length}`);
  analysis.beforeAfterPoints.slice(0, 3).forEach((p, i) => {
    console.log(`  ${i + 1}. [${p.timestamp}] ${p.state}`);
  });

  console.log(`\n💡 Recommendations:`);
  analysis.recommendations.forEach(r => console.log(`  • ${r}`));

  console.log(`\n${'='.repeat(60)}\n`);
}

async function main() {
  const videoPath = process.argv[2];

  if (!videoPath) {
    console.log(`Usage: node video-analyzer.js <video-file>`);
    console.log(`\nExample: node video-analyzer.js boat-detail.mp4`);
    console.log(`\nOutput: Creates a JSON edit plan with:`);
    console.log(`  • Key frame timestamps for cuts`);
    console.log(`  • Before/after detection`);
    console.log(`  • Hook suggestions from your bank`);
    console.log(`  • CTA recommendations`);
    process.exit(1);
  }

  if (!fs.existsSync(videoPath)) {
    console.error(`❌ File not found: ${videoPath}`);
    process.exit(1);
  }

  const outputDir = path.join(path.dirname(videoPath), 'frames_temp');
  const manifestPath = path.join(path.dirname(videoPath), `${path.basename(videoPath, path.extname(videoPath))}_edit-plan.json`);

  try {
    // Extract frames
    const frames = await extractFrames(videoPath, outputDir, 5);

    // Analyze frames
    const analysis = await analyzeFrames(frames, outputDir);

    // Generate plan
    const plan = generateEditPlan(analysis, videoPath);

    // Output manifest
    const manifest = outputEditManifest(plan, videoPath, manifestPath);

    // Print summary
    printReport(plan);

    console.log(`📂 Next steps:`);
    console.log(`  1. Open ${path.basename(manifestPath)} in your editor`);
    console.log(`  2. Use timestamps to mark cuts in CapCut/Premiere/DaVinci`);
    console.log(`  3. Add the suggested hook as caption`);
    console.log(`  4. Export 3 versions (long/short/carousel)`);

    // Cleanup
    execSync(`rm -rf "${outputDir}"`, { stdio: 'pipe' });

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
