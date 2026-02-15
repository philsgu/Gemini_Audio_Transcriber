# 🎤 Audio Transcriber CLI

A powerful command-line tool that converts MP3 files into polished markdown transcripts using Google's Gemini AI.

## ✨ Features

- 🎵 **MP3 to Text**: Automatic transcription of audio files
- 🤖 **AI Polishing**: Uses Gemini AI to clean up and improve transcripts
- 📊 **Progress Tracking**: Real-time percentage completion indicators
- 📝 **Markdown Output**: Professional formatted output files
- ⚙️ **Customizable**: Custom prompts and formatting options
- 🌍 **Global CLI**: Install once, use anywhere

## 🔧 Prerequisites

### System Requirements

1. **Python 3.7+**
2. **FFmpeg** (required for audio processing)

#### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to your system PATH

### Gemini API Key

You'll need a Google Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Save it securely

## 📦 Installation

### Option 1: Install Globally (Recommended)

```bash
# Clone or download the repository
cd audio-transcriber-cli

# Install the package globally
pip install -e .
```

Now you can use `audio-transcribe` command from anywhere!

### Option 2: Install Dependencies Only

```bash
pip install -r requirements.txt
python audio_transcriber.py [arguments]
```

## 🚀 Usage

### Set Your API Key

**Option A: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Add to your `~/.bashrc` or `~/.zshrc` to make it permanent:
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Option B: Pass as Argument**
```bash
audio-transcribe input.mp3 --api-key "your-api-key-here"
```

### Basic Usage

```bash
# Simple transcription
audio-transcribe podcast.mp3

# Specify output file
audio-transcribe podcast.mp3 -o transcript.md

# Add a custom title
audio-transcribe podcast.mp3 --title "My Awesome Podcast Episode"

# Custom polishing prompt
audio-transcribe interview.mp3 --prompt "Summarize the key points and create bullet points"
```

### Command Line Options

```
positional arguments:
  input_file            Path to the MP3 file

optional arguments:
  -h, --help           Show this help message and exit
  -o, --output         Output markdown file path
  -t, --title          Title for the markdown document
  -p, --prompt         Custom prompt for Gemini AI polishing
  --api-key            Gemini API key (or set GEMINI_API_KEY env var)
  --keep-temp          Keep temporary WAV file
```

## 📊 Progress Indicators

The tool shows real-time progress for each step:

```
🔄 Converting MP3 to WAV format...
✅ Conversion complete

🎤 Transcribing audio to text...
Transcription progress: 100%|████████████████| 100/100 [00:45<00:00]
✅ Transcription complete

✨ Polishing transcript with Gemini AI...
AI polishing: 100%|████████████████████████████| 100/100 [00:05<00:00]
✅ Polishing complete

💾 Saving to podcast_transcript.md...
✅ File saved successfully

✨ SUCCESS! Transcript saved to: podcast_transcript.md
```

## 📝 Example Output

The tool generates clean markdown files like this:

```markdown
# My Podcast Episode

This is the polished transcript with proper grammar, 
punctuation, and formatting. All filler words have been 
removed and the content flows naturally.

The AI organizes the content into logical paragraphs 
and ensures professional presentation.
```

## 🎨 Custom Prompts

You can customize how Gemini polishes your transcript:

```bash
# Create a summary instead
audio-transcribe meeting.mp3 --prompt "Create a concise summary with action items"

# Format for blog post
audio-transcribe interview.mp3 --prompt "Convert this interview into a blog post format with Q&A structure"

# Extract key points
audio-transcribe lecture.mp3 --prompt "Extract the main concepts and create a study guide"
```

## ⚠️ Limitations

- **Audio Length**: Very long files (>1 hour) may take significant time to process
- **Audio Quality**: Clear audio produces better transcriptions
- **Language**: Currently optimized for English (Google Speech Recognition default)
- **API Costs**: Gemini API usage may incur costs depending on your plan

## 🔍 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
Install FFmpeg using the instructions in Prerequisites section.

### "API key not found"
Set your `GEMINI_API_KEY` environment variable or pass it via `--api-key`.

### Poor transcription quality
- Ensure audio is clear and not too noisy
- Check that audio volume is adequate
- Consider pre-processing audio to improve quality

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use this tool for personal or commercial projects.

## 🙏 Acknowledgments

- Google Gemini AI for text polishing
- Google Speech Recognition for transcription
- pydub for audio processing

---

Made with ❤️ by the community
