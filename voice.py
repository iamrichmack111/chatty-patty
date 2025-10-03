#!/usr/bin/env python3
import argparse
import os
import re
from TTS.api import TTS
from playsound import playsound
from tqdm import tqdm  # progress bar

VOICE_MODELS = {
    "female_en": "tts_models/en/ljspeech/glow-tts",   # Single-speaker female
    "male_en": "tts_models/en/vctk/vits",             # Multi-speaker English
    "multilingual": "tts_models/multilingual/multi-dataset/xtts_v2",  # Accents/languages
}

# --- Text Cleaning ---
def clean_text(text: str) -> str:
    # Remove non-ASCII/unusual chars (IPA, emojis, etc.)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --- Chunking Long Text ---
def chunk_text(text: str, max_chars: int = 500) -> list[str]:
    """Split long text into safe chunks for TTS."""
    sentences = re.split(r'(?<=[.!?]) +', text)  # split at sentence boundaries
    chunks, current = [], ""
    for s in sentences:
        s = clean_text(s)
        if len(s) < 5:  # skip too-short lines
            continue
        if len(current) + len(s) < max_chars:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = s
    if current:
        chunks.append(current.strip())
    return chunks

def main():
    parser = argparse.ArgumentParser(description="🎙️ Text-to-Speech with Coqui TTS")
    parser.add_argument("--text", type=str, help="Text to read")
    parser.add_argument("--file", type=str, help="Path to text file")
    parser.add_argument("--out", type=str, default="output.wav", help="Output file")
    parser.add_argument("--mp3", action="store_true", help="Save as MP3 instead of WAV")
    parser.add_argument("--voice", type=str, default="female_en", choices=VOICE_MODELS.keys())
    parser.add_argument("--speaker_wav", type=str, help="Reference voice sample (XTTS only)")
    parser.add_argument("--speaker", type=str, help="Speaker ID (for multispeaker models)")
    parser.add_argument("--list_speakers", action="store_true", help="List speakers for model")
    parser.add_argument("--no_play", action="store_true", help="Skip auto-playback")
    args = parser.parse_args()

    model_name = VOICE_MODELS[args.voice]
    tts = TTS(model_name)

    # --- List Speakers ---
    if args.list_speakers:
        if hasattr(tts, "speakers") and tts.speakers:
            print(f"🎙️ Speakers for {args.voice}:")
            for s in tts.speakers:
                print(" -", s)
        else:
            print(f"ℹ️ No speaker list available for {args.voice}. Use --speaker_wav instead.")
        return

    # --- Load Input ---
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    elif args.text:
        raw_text = args.text
    else:
        print("❌ Please provide --text or --file")
        return

    # --- Prepare Output ---
    out_file = args.out
    if args.mp3 and not out_file.endswith(".mp3"):
        out_file = os.path.splitext(out_file)[0] + ".mp3"

    # --- Split into chunks ---
    chunks = chunk_text(raw_text)
    if not chunks:
        print("❌ No valid text to synthesize after cleaning.")
        return

    print(f"📖 Processing {len(chunks)} chunks with {args.voice}...")

    # --- Generate Audio ---
    wavs = []
    for i, chunk in enumerate(tqdm(chunks, desc="Synthesizing")):
        if "xtts" in model_name.lower():  # multilingual XTTS
            if args.speaker_wav:
                wavs.append(tts.tts(chunk, speaker_wav=args.speaker_wav, language="en"))
            else:
                speaker = args.speaker or "default"
                wavs.append(tts.tts(chunk, speaker=speaker, language="en"))
        elif "vctk" in model_name.lower():  # male_en (VCTK)
            speaker = args.speaker or "p225"  # fallback default speaker
            wavs.append(tts.tts(chunk, speaker=speaker))
        else:  # female_en (Glow-TTS single voice)
            wavs.append(tts.tts(chunk))

    # Save concatenated output
    tts.save_wav(wavs, out_file)
    print(f"✅ Done! Saved {out_file}")

    if not args.no_play:
        playsound(out_file)

if __name__ == "__main__":
    main()

