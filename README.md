Perfect 👍 let’s make your **README.md** polished and user-friendly so anyone can grab **Chatty-Patty** and run it.
I’ll include a **banner screenshot**, **dependencies**, **installation instructions**, **usage examples**, and **sample commands**.

---

## 📄 README.md for `chatty-patty`

````markdown
# 🎙️ Chatty-Patty

![Chatty-Patty Banner](https://user-images.githubusercontent.com/iamrichmack111/placeholder.png)

**Chatty-Patty** is a fun, free, and lightweight text-to-speech narrator written in Python.  
It uses [gTTS](https://pypi.org/project/gTTS/) (Google Text-to-Speech) to read text files aloud with natural voices, no API keys or paid services required.  

✨ Features:
- ✅ **Free & local** – uses gTTS, no billing or API keys
- ✅ **Multi-colored CLI output** with [colorama](https://pypi.org/project/colorama/)
- ✅ **ASCII art banner** using [pyfiglet](https://pypi.org/project/pyfiglet/)
- ✅ **Markdown/asterisk cleanup** for smoother narration
- ✅ **Safe chunking** for long files (gTTS limit ~5000 chars)
- ✅ **Dual voice mode** – alternate between two accents/languages for a podcast-style effect
- ✅ Outputs to **MP3 narration files**

---

## 📦 Installation

Clone the repository:

```bash
git clone git@github.com:iamrichmack111/chatty-patty.git
cd chatty-patty
````

Install dependencies:

```bash
pip install -r requirements.txt
```

If you don’t have `ffmpeg` installed (needed by `pydub`):

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg -y

# macOS (Homebrew)
brew install ffmpeg
```

---

## 📚 Dependencies

All dependencies are listed in `requirements.txt`:

```
gTTS
pydub
tqdm
colorama
pyfiglet
```

---

## 🚀 Usage

Run `narrator.py` with your text file:

```bash
python3 narrator.py --file mybook.txt --out narration.mp3 --lang1 en
```

### 🔹 Options

| Flag          | Description                                                                              |
| ------------- | ---------------------------------------------------------------------------------------- |
| `--file`      | Input text file (UTF-8) to narrate.                                                      |
| `--out`       | Output MP3 file name. Default: `narration.mp3`.                                          |
| `--lang1`     | Primary language code (default: `en` for US English).                                    |
| `--lang2`     | Optional secondary language code. If set, Chatty-Patty alternates voices chunk-by-chunk. |
| `--max_chars` | Maximum characters per chunk (default: 4000, gTTS hard limit ~5000).                     |

---

## 🎧 Examples

### 1. Single voice (US English)

```bash
python3 narrator.py --file ../bookrag/game.txt --out game.mp3 --lang1 en
```

### 2. Dual voices (alternate chunks: US English ↔ British English)

```bash
python3 narrator.py --file ../bookrag/game.txt --out game.mp3 \
  --lang1 en --lang2 en-uk
```

### 3. Narrate with Australian accent

```bash
python3 narrator.py --file story.md --out story_au.mp3 --lang1 en-au
```

### 4. Shorter chunks for smoother handling

```bash
python3 narrator.py --file long_text.txt --out long_text.mp3 --lang1 en --max_chars 3000
```

---

## 🖼️ Sample Output

When you run Chatty-Patty:

```
   ____ _           _   _           ____      _   _       
  / ___| |__   __ _| |_| |_ _   _  |  _ \ ___| |_| |_ ___ 
 | |   | '_ \ / _` | __| __| | | | | |_) / _ \ __| __/ _ \
 | |___| | | | (_| | |_| |_| |_| | |  __/  __/ |_| ||  __/
  \____|_| |_|\__,_|\__|\__|\__, | |_|   \___|\__|\__\___|
                            |___/                          

💬 Your free offline narrator with gTTS!

📖 Narrating 52 chunks → narration.mp3
Synthesizing: 100%|██████████████████████████████| 52/52 [00:54<00:00,  1.05s/chunk]
✅ Done! Narration saved as narration.mp3
```

---

## 👤 Author

**Jeremy Franklin**
GitHub: [@iamrichmack111](https://github.com/iamrichmack111)

---

## 📜 License

This project is MIT licensed. See the [LICENSE](LICENSE) file for details.

```

---

```

