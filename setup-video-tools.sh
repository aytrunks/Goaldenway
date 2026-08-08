#!/bin/bash

set -e

echo "🚀 Setting up Goaldenway Video Tools"
echo "===================================="

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from https://nodejs.org"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found. Install with:"
    echo "   Mac: brew install ffmpeg"
    echo "   Linux: sudo apt install ffmpeg"
    echo "   Windows: choco install ffmpeg"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ ffmpeg found: $(ffmpeg -version | head -1)"
fi

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo "Get a free key from: https://console.anthropic.com/api_keys"
    echo ""
    read -p "Enter your API key (sk-ant-...): " api_key
    if [ -z "$api_key" ]; then
        echo "Skipping for now. Set later with: export ANTHROPIC_API_KEY=sk-ant-..."
    else
        export ANTHROPIC_API_KEY="$api_key"
        echo "export ANTHROPIC_API_KEY=\"$api_key\"" >> ~/.bashrc
        echo "✅ API key saved to ~/.bashrc"
    fi
else
    echo "✅ ANTHROPIC_API_KEY is set"
fi

# Install npm dependencies
echo ""
echo "📦 Installing npm dependencies..."
npm install @anthropic-ai/sdk --save --quiet

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Usage:"
echo "   node video-analyzer.js <video-file>"
echo "   node video-caption-generator.js <edit-plan-json>"
echo ""
echo "📚 Documentation: cat VIDEO_TOOLS_README.md"
echo ""
