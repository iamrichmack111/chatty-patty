#!/usr/bin/env python3
import argparse, re, os, sys
from tqdm import tqdm
from gtts import gTTS
from pydub import AudioSegment
from pyfiglet import Figlet
from colorama import Fore, Style, init

init(autoreset=True)

# --------- text cleaning ----------
def clean_text(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"`+([^`]+)`+", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r":[a-z_]+:", "", text)
    text = re.sub(r"[#*_~`>]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# --------- safe chunking for gTTS ----------
def chunk_text(text, max_chars=4000):
    words, chunks, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 < max_chars:
            cur += " " + w
        else:
            chunks.append(cur.strip()); cur = w
    if cur: chunks.append(cur.strip())
    return chunks

def synthesize_chunk(text, lang, tmpfile):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(tmpfile)

def main():
    # ---- Fancy Banner ----
    fig = Figlet(font="slant")
    print(Fore.CYAN + fig.renderText("Chatty-Patty"))
    print(Fore.YELLOW + "💬 Your free offline narrator with gTTS!\n")

    # ---- Argument parser with rich help ----
    ap = argparse.ArgumentParser(
        prog="Chatty-Patty",
        description="🎙️ A colorful TTS narrator that reads text files aloud using gTTS.\n"
                    "Supports single or dual 'voices' (different language accents), "
                    "cleans up Markdown, and stitches into one MP3.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    ap.add_argument("--file", required=True,
                    help="Path to input text file (UTF-8).")
    ap.add_argument("--out", default="narration.mp3",
                    help="Output MP3 filename.")
    ap.add_argument("--lang1", default="en",
                    help="Primary language code (e.g. 'en' for US English).")
    ap.add_argument("--lang2",
                    help="Optional secondary language code. If set, voices alternate per chunk.")
    ap.add_argument("--max_chars", type=int, default=4000,
                    help="Maximum characters per chunk (gTTS limit ~5000).")
    args = ap.parse_args()

    # ---- Load + clean ----
    if not os.path.exists(args.file):
        print(Fore.RED + f"❌ File not found: {args.file}")
        sys.exit(1)

    raw = open(args.file, encoding="utf-8").read()
    text = clean_text(raw)
    chunks = chunk_text(text, max_chars=args.max_chars)

    if not chunks:
        print(Fore.RED + "❌ Nothing to narrate after cleaning.")
        sys.exit(1)

    # ---- Narration ----
    print(Fore.GREEN + f"📖 Narrating {len(chunks)} chunks → {args.out}")
    audio_segments = []

    for i, chunk in enumerate(tqdm(chunks, desc="Synthesizing", unit="chunk")):
        lang = args.lang1 if not args.lang2 else (args.lang1 if i % 2 == 0 else args.lang2)
        tmp = f"tmp_{i}.mp3"
        synthesize_chunk(chunk, lang, tmp)
        audio_segments.append(AudioSegment.from_mp3(tmp))
        os.remove(tmp)

    final = sum(audio_segments[1:], audio_segments[0])
    final.export(args.out, format="mp3")

    print(Fore.MAGENTA + f"✅ Done! Narration saved as {args.out}\n")
    print(Fore.CYAN + "Tips:")
    print("  " + Fore.YELLOW + "--lang1 en --lang2 en-uk" + Fore.WHITE + " → alternate US/UK English")
    print("  " + Fore.YELLOW + "--lang1 en --lang2 en-au" + Fore.WHITE + " → alternate US/Australian")
    print("  " + Fore.YELLOW + "--max_chars 3000" + Fore.WHITE + " → smaller chunks (smoother narration)")

if __name__ == "__main__":
    main()

