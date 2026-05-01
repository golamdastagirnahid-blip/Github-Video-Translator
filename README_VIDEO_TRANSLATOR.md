# Free Video Translator 🎬🌍

A completely free, open-source video translation tool that translates videos from any language to any language using open-source AI models.

## Features

- ✅ **Speech-to-Text**: OpenAI Whisper (excellent accuracy, 90+ languages)
- ✅ **Translation**: LibreTranslate / Argos Translate (free, open-source)
- ✅ **Text-to-Speech**: Edge TTS / Coqui TTS (natural voices, 80+ languages)
- ✅ **Video Processing**: MoviePy (seamless audio replacement)
- ✅ **GPU Support**: CUDA acceleration for faster processing
- ✅ **GitHub Actions**: Run in the cloud (with limitations)

## Supported Languages

**90+ languages including:**
- English, Spanish, French, German, Italian, Portuguese
- Russian, Japanese, Korean, Chinese, Arabic, Hindi
- Turkish, Polish, Dutch, Swedish, Danish, Finnish
- Ukrainian, Czech, Romanian, Hungarian, Bengali
- Tamil, Telugu, Marathi, Urdu, Persian, Swahili
- And many more...

## Installation

### Local Installation

```bash
# Clone or download video_translator.py
# Install dependencies
pip install -r requirements.txt

# For GPU acceleration (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### System Requirements

- Python 3.8+
- FFmpeg (required for video processing)
  - Windows: Download from https://ffmpeg.org/download.html
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

## Usage

### Basic Usage

```bash
# Translate video to Spanish
python video_translator.py input.mp4 --target-lang es

# Translate to French
python video_translator.py input.mp4 --target-lang fr

# Specify output file
python video_translator.py input.mp4 --target-lang de -o output_german.mp4
```

### Advanced Options

```bash
# Use better Whisper model (slower but more accurate)
python video_translator.py input.mp4 --target-lang es --whisper-model small

# Use Coqui TTS for better voice quality
python video_translator.py input.mp4 --target-lang fr --tts coqui

# Use GPU acceleration
python video_translator.py input.mp4 --target-lang de --device cuda

# Keep temporary files for debugging
python video_translator.py input.mp4 --target-lang es --keep-temp
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--target-lang`, `-t` | Target language code (required) | - |
| `--output`, `-o` | Output video path | `input_translated_LANG.mp4` |
| `--whisper-model`, `-m` | Whisper model size | `base` |
| `--device`, `-d` | Device to use | `auto` |
| `--tts-engine` | TTS engine (`edge` or `coqui`) | `edge` |
| `--translation-engine` | Translation engine | `auto` |
| `--keep-temp` | Keep temporary files | `false` |

### Whisper Model Sizes

| Model | Size | Speed | Accuracy | VRAM |
|-------|------|-------|----------|------|
| `tiny` | ~40MB | ⚡⚡⚡ | Good | ~1GB |
| `base` | ~75MB | ⚡⚡ | Very Good | ~1GB |
| `small` | ~250MB | ⚡ | Excellent | ~2GB |
| `medium` | ~770MB | Moderate | Excellent | ~5GB |
| `large` | ~1.5GB | Slow | Best | ~10GB |

## GitHub Actions Usage

### Manual Trigger

1. Go to your repository's **Actions** tab
2. Select **Video Translator** workflow
3. Click **Run workflow**
4. Enter:
   - Video URL (must be publicly accessible)
   - Target language code
   - Whisper model size
5. Download the translated video from **Artifacts**

### Example Workflow Trigger

```yaml
# In your .github/workflows/video-translator.yml
on:
  workflow_dispatch:
    inputs:
      video_url:
        description: 'URL of video to translate'
        required: true
      target_lang:
        description: 'Target language (e.g., es, fr, de)'
        required: true
        default: 'es'
```

## GitHub Actions Limitations

⚠️ **Important: GitHub Actions has limitations:**

| Limitation | Details |
|------------|---------|
| **No GPU** | CPU-only processing (slower) |
| **Time limit** | 6 hours per job |
| **Monthly limit** | 35 hours total (free tier) |
| **Storage** | Artifacts expire after 7 days |
| **Video size** | Large videos may timeout |

**Recommendation:** For production use, run locally or use a GPU-enabled platform.

## Translation Engines

The tool tries multiple translation engines in order:

1. **LibreTranslate** (local instance or public API)
2. **Argos Translate** (offline, 100+ language pairs)
3. **Google Translate** (via translatepy)

### Setting Up LibreTranslate (Local)

```bash
# Install LibreTranslate
pip install libretranslate

# Run local server
libretranslate --host localhost --port 5000
```

## TTS Engines

### Edge TTS (Default)

- ✅ Fast generation
- ✅ 80+ languages
- ✅ Natural voices
- ✅ No API key needed

### Coqui TTS (Optional)

- ✅ Better voice quality
- ✅ Emotion control
- ✅ Voice cloning
- ⚠️ Slower generation
- ⚠️ Larger download

```bash
# Install Coqui TTS
pip install TTS

# Use with --tts coqui
python video_translator.py input.mp4 --target-lang es --tts coqui
```

## Examples

### Example 1: Quick Translation

```bash
python video_translator.py tutorial.mp4 --target-lang es
```

Output: `tutorial_translated_es.mp4`

### Example 2: High Quality Translation

```bash
python video_translator.py \
  presentation.mp4 \
  --target-lang fr \
  --whisper-model small \
  --tts coqui \
  --device cuda
```

### Example 3: Batch Translation

```bash
# Translate to multiple languages
for lang in es fr de it pt; do
  python video_translator.py video.mp4 --target-lang $lang
done
```

## Troubleshooting

### FFmpeg not found

```
Error: ffmpeg not found
```

**Solution:** Install FFmpeg for your OS

### Out of memory

```
CUDA out of memory
```

**Solution:** Use smaller Whisper model or CPU mode
```bash
python video_translator.py input.mp4 --target-lang es --device cpu --whisper-model tiny
```

### Translation failed

```
⚠ Translation failed, using original text
```

**Solution:** Install translation engine
```bash
pip install libretranslatepy argostranslate
```

### GitHub Actions timeout

**Solution:** Use smaller video or smaller Whisper model
```bash
--whisper-model tiny
```

## Performance

| Configuration | 1-min video | 5-min video | 10-min video |
|---------------|-------------|-------------|--------------|
| CPU + tiny | ~2 min | ~10 min | ~20 min |
| CPU + base | ~5 min | ~25 min | ~50 min |
| GPU + base | ~1 min | ~5 min | ~10 min |
| GPU + small | ~2 min | ~10 min | ~20 min |

## License

This tool uses open-source components with permissive licenses:

- **Whisper**: MIT License
- **MoviePy**: MIT License
- **Edge TTS**: MIT License
- **LibreTranslate**: AGPL-3.0
- **Argos Translate**: MIT License

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [MoviePy](https://github.com/Zulko/moviepy) - Video editing
- [Edge TTS](https://github.com/rany2/edge-tts) - Text-to-speech
- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) - Translation
- [Argos Translate](https://github.com/argosopentech/argos-translate) - Translation

## Disclaimer

This tool is provided as-is for educational and personal use. The quality of translation depends on:
- Audio quality of input video
- Language pair availability
- Model accuracy

For professional use, consider commercial solutions.
