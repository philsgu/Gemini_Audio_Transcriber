#!/usr/bin/env python3
"""
Audio Transcriber CLI Tool
Converts MP3 files to text, polishes with Gemini AI, and outputs markdown
"""

import os
import sys
import argparse
from pathlib import Path
import google.generativeai as genai
from pydub import AudioSegment
import speech_recognition as sr
from tqdm import tqdm
import math


class AudioTranscriber:
    def __init__(self, api_key: str):
        """Initialize the transcriber with Gemini API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.recognizer = sr.Recognizer()

    def convert_mp3_to_wav(self, mp3_path: str, output_path: str = None) -> str:
        """Convert MP3 to WAV format for speech recognition"""
        print("🔄 Converting MP3 to WAV format...")

        if output_path is None:
            output_path = mp3_path.rsplit(".", 1)[0] + "_temp.wav"

        audio = AudioSegment.from_mp3(mp3_path)
        # Optimize for speech recognition: 16kHz sample rate, mono, 16-bit
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export(output_path, format="wav")

        print("✅ Conversion complete")
        return output_path

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio file to text with progress tracking"""
        print("\n🎤 Transcribing audio to text...")

        # Load audio file
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_duration = source.DURATION

            # Calculate chunks (process in 60-second segments for better context)
            chunk_duration = 60  # seconds
            num_chunks = math.ceil(audio_duration / chunk_duration)

            transcription_parts = []

            with tqdm(total=100, desc="Transcription progress", unit="%") as pbar:
                for i in range(num_chunks):
                    offset = i * chunk_duration
                    duration = min(chunk_duration, audio_duration - offset)

                    # Read audio chunk
                    audio_data = self.recognizer.record(
                        source, duration=duration, offset=offset
                    )

                    try:
                        # Transcribe chunk using Google Speech Recognition with language hint
                        text = self.recognizer.recognize_google(
                            audio_data, language="en-US", show_all=False
                        )
                        if text.strip():  # Only add non-empty transcriptions
                            transcription_parts.append(text)
                    except sr.UnknownValueError:
                        # Skip inaudible sections rather than marking them
                        pass
                    except sr.RequestError as e:
                        print(f"\n⚠️  Error with speech recognition service: {e}")
                        print("Continuing with remaining audio...")

                    # Update progress
                    progress = int(((i + 1) / num_chunks) * 100)
                    pbar.update(progress - pbar.n)

        if not transcription_parts:
            raise Exception(
                "No audio could be transcribed. Check audio quality and format."
            )

        full_transcription = " ".join(transcription_parts)
        print("✅ Transcription complete")
        return full_transcription

    def polish_with_gemini(self, transcript: str, custom_prompt: str = None) -> str:
        """Polish the transcript using Gemini AI"""
        print("\n✨ Polishing transcript with Gemini AI...")

        default_prompt = """
Please polish and improve this transcript. Your tasks:

1. Fix grammar, punctuation, and spelling errors
2. Improve sentence structure and flow
3. Remove filler words (um, uh, like, you know, etc.)
4. Add proper paragraph breaks for better readability - start new paragraphs when topics change
5. Organize content into logical sections if multiple topics are discussed
6. Maintain the original meaning and tone
7. Format as clean, professional markdown text with proper spacing

Important: Keep all factual information and technical terms exactly as stated. Only improve the formatting and readability.

Transcript to polish:
"""

        prompt = custom_prompt if custom_prompt else default_prompt
        full_prompt = f"{prompt}\n\n{transcript}"

        try:
            with tqdm(total=100, desc="AI polishing", unit="%") as pbar:
                pbar.update(20)
                response = self.model.generate_content(full_prompt)
                pbar.update(60)
                polished_text = response.text
                pbar.update(20)

            print("✅ Polishing complete")
            return polished_text

        except Exception as e:
            print(f"\n⚠️  Error with Gemini API: {e}")
            print("Returning original transcript...")
            return transcript

    def save_as_markdown(self, content: str, output_path: str, title: str = None):
        """Save the polished content as a markdown file"""
        print(f"\n💾 Saving to {output_path}...")

        with open(output_path, "w", encoding="utf-8") as f:
            if title:
                f.write(f"# {title}\n\n")
            f.write(content)

        print("✅ File saved successfully")

    def process_audio_file(
        self,
        mp3_path: str,
        output_path: str = None,
        title: str = None,
        custom_prompt: str = None,
        keep_temp: bool = False,
    ):
        """Main pipeline to process audio file"""

        print(f"\n{'='*60}")
        print(f"🎵 Processing: {mp3_path}")
        print(f"{'='*60}\n")

        # Set default output path
        if output_path is None:
            output_path = Path(mp3_path).stem + "_transcript.md"

        # Set default title
        if title is None:
            title = Path(mp3_path).stem.replace("_", " ").title()

        try:
            # Step 1: Convert to WAV (10% progress)
            wav_path = self.convert_mp3_to_wav(mp3_path)

            # Step 2: Transcribe (50% progress)
            transcript = self.transcribe_audio(wav_path)

            # Step 3: Polish with Gemini (30% progress)
            polished_content = self.polish_with_gemini(transcript, custom_prompt)

            # Step 4: Save as markdown (10% progress)
            self.save_as_markdown(polished_content, output_path, title)

            # Cleanup temp WAV file
            if not keep_temp and wav_path.endswith("_temp.wav"):
                os.remove(wav_path)
                print(f"🗑️  Cleaned up temporary file: {wav_path}")

            print(f"\n{'='*60}")
            print(f"✨ SUCCESS! Transcript saved to: {output_path}")
            print(f"{'='*60}\n")

        except Exception as e:
            print(f"\n❌ Error processing file: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Convert MP3 to polished markdown transcript using Gemini AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  audio-transcribe input.mp3
  audio-transcribe input.mp3 -o output.md
  audio-transcribe input.mp3 --title "My Podcast Episode"
  audio-transcribe input.mp3 --prompt "Summarize the key points"
        """,
    )

    parser.add_argument("input_file", help="Path to the MP3 file")
    parser.add_argument("-o", "--output", help="Output markdown file path")
    parser.add_argument("-t", "--title", help="Title for the markdown document")
    parser.add_argument("-p", "--prompt", help="Custom prompt for Gemini AI polishing")
    parser.add_argument(
        "--api-key", help="Gemini API key (or set GEMINI_API_KEY env var)"
    )
    parser.add_argument(
        "--keep-temp", action="store_true", help="Keep temporary WAV file"
    )

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: Gemini API key not found!")
        print(
            "Please provide it via --api-key or set GEMINI_API_KEY environment variable"
        )
        sys.exit(1)

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"❌ Error: File not found: {args.input_file}")
        sys.exit(1)

    # Initialize and process
    transcriber = AudioTranscriber(api_key)
    transcriber.process_audio_file(
        mp3_path=args.input_file,
        output_path=args.output,
        title=args.title,
        custom_prompt=args.prompt,
        keep_temp=args.keep_temp,
    )


if __name__ == "__main__":
    main()
