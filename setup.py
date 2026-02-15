from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="audio-transcriber-cli",
    version="1.0.0",
    author="Your Name",
    description="Convert MP3 files to polished markdown transcripts using Gemini AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audio-transcriber-cli",
    py_modules=["audio_transcriber"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-generativeai>=0.3.0",
        "pydub>=0.25.1",
        "SpeechRecognition>=3.10.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "audio-transcribe=audio_transcriber:main",
        ],
    },
)
