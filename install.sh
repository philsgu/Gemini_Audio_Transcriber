#!/bin/bash

# Audio Transcriber CLI - Quick Installation Script

echo "🎤 Audio Transcriber CLI - Installation Script"
echo "=============================================="
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check FFmpeg installation
echo "Checking FFmpeg installation..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed."
    echo ""
    echo "Please install FFmpeg:"
    echo "  macOS:    brew install ffmpeg"
    echo "  Ubuntu:   sudo apt install ffmpeg"
    echo "  Windows:  Download from ffmpeg.org"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg is installed"
fi
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Install the CLI tool globally
echo "Installing audio-transcribe CLI globally..."
pip3 install -e .

if [ $? -ne 0 ]; then
    echo "❌ Failed to install CLI tool"
    exit 1
fi

echo "✅ CLI tool installed"
echo ""

# Check for API key
echo "Checking for Gemini API key..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY environment variable is not set."
    echo ""
    echo "To set your API key permanently, run:"
    echo "  echo 'export GEMINI_API_KEY=\"your-api-key\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    echo "Or pass it as an argument: audio-transcribe file.mp3 --api-key \"your-key\""
else
    echo "✅ API key is configured"
fi

echo ""
echo "=============================================="
echo "✨ Installation complete!"
echo ""
echo "Usage:"
echo "  audio-transcribe your-audio.mp3"
echo ""
echo "For more options:"
echo "  audio-transcribe --help"
echo "=============================================="
