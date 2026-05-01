# 🎬 Free Video Translator

> Translate videos from any language to any language - 100% free and open-source

![GitHub](https://img.shields.io/github/license/yourusername/video-translator)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🌍 **90+ Languages** supported
- 🎯 **High Accuracy** using OpenAI Whisper
- 🆓 **100% Free** - no API keys required
- 🚀 **GPU Acceleration** support
- 🔄 **GitHub Actions** ready
- 💻 **Cross-platform** (Windows, Mac, Linux)

## 📦 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Translate a video
python video_translator.py input.mp4 --target-lang es
```

## 🌐 Supported Languages

English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi, Turkish, Polish, Dutch, Swedish, Danish, Finnish, Ukrainian, Czech, Romanian, Hungarian, Bengali, Tamil, Telugu, Marathi, Urdu, Persian, Swahili, and 70+ more.

## 📖 Documentation

See [README_VIDEO_TRANSLATOR.md](README_VIDEO_TRANSLATOR.md) for full documentation.

## 🚀 GitHub Actions

This repository includes a GitHub Actions workflow that allows you to translate videos in the cloud.

### Usage

1. Go to the **Actions** tab
2. Select **Video Translator** workflow
3. Click **Run workflow**
4. Enter the video URL and target language
5. Download the translated video from Artifacts

## 📁 Project Structure

```
Github Translator/
├── .github/
│   └── workflows/
│       └── video-translator.yml    # GitHub Actions workflow
├── video_translator.py             # Main translation tool
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── README_VIDEO_TRANSLATOR.md      # Full documentation
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Speech-to-Text | OpenAI Whisper |
| Translation | LibreTranslate / Argos Translate |
| Text-to-Speech | Edge TTS / Coqui TTS |
| Video Processing | MoviePy |

## ⚡ Performance

| Configuration | 1-min video | 5-min video |
|---------------|-------------|-------------|
| CPU + tiny | ~2 min | ~10 min |
| CPU + base | ~5 min | ~25 min |
| GPU + base | ~1 min | ~5 min |

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## ⚠️ Disclaimer

This tool is provided as-is for educational and personal use. Translation quality depends on audio quality and language pair availability.

---

Made with ❤️ using open-source AI
