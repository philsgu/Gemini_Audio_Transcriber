#!/usr/bin/env python3
"""
Example usage of the Audio Transcriber CLI
This demonstrates how to use the tool programmatically
"""

from audio_transcriber import AudioTranscriber
import os

def example_basic_usage():
    """Basic usage example"""
    # Get API key from environment
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    # Initialize transcriber
    transcriber = AudioTranscriber(api_key)
    
    # Process an audio file
    transcriber.process_audio_file(
        mp3_path="sample_audio.mp3",
        output_path="transcript.md",
        title="My Audio Transcript"
    )


def example_custom_prompt():
    """Example with custom polishing prompt"""
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    transcriber = AudioTranscriber(api_key)
    
    custom_prompt = """
    Please convert this transcript into a professional meeting summary with:
    1. Key discussion points
    2. Action items
    3. Decisions made
    4. Next steps
    
    Format as a structured document.
    
    Transcript:
    """
    
    transcriber.process_audio_file(
        mp3_path="meeting.mp3",
        output_path="meeting_summary.md",
        title="Team Meeting Summary",
        custom_prompt=custom_prompt
    )


def example_batch_processing():
    """Process multiple files"""
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    transcriber = AudioTranscriber(api_key)
    
    audio_files = [
        "episode_01.mp3",
        "episode_02.mp3",
        "episode_03.mp3"
    ]
    
    for audio_file in audio_files:
        output_name = audio_file.replace('.mp3', '_transcript.md')
        print(f"\nProcessing: {audio_file}")
        
        try:
            transcriber.process_audio_file(
                mp3_path=audio_file,
                output_path=output_name
            )
        except Exception as e:
            print(f"Error processing {audio_file}: {e}")
            continue


if __name__ == "__main__":
    print("Audio Transcriber - Example Usage")
    print("=" * 50)
    print("\n1. Basic usage")
    print("2. Custom prompt")
    print("3. Batch processing")
    
    choice = input("\nSelect example (1-3): ")
    
    if choice == "1":
        example_basic_usage()
    elif choice == "2":
        example_custom_prompt()
    elif choice == "3":
        example_batch_processing()
    else:
        print("Invalid choice")
