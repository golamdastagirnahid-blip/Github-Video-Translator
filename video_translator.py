"""
Free Video Translator
Translate videos from any language to any language using open-source tools.

Features:
- Speech-to-text: OpenAI Whisper (free, excellent quality)
- Translation: LibreTranslate / Argos Translate (free, open-source)
- Text-to-speech: Coqui TTS / Edge TTS (free, open-source)
- Video processing: MoviePy (free, open-source)

Requirements:
    pip install whisper openai-whisper moviepy edge-tts
    pip install libretranslate argostranslate translatepy

For GPU acceleration (optional):
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

Usage:
    python video_translator.py input.mp4 --target-lang es --output output.mp4
"""

import os
import sys
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple
import warnings
warnings.filterwarnings("ignore")


class VideoTranslator:
    """Free video translation tool using open-source libraries."""

    def __init__(
        self,
        whisper_model: str = "base",
        device: str = "auto",
        tts_engine: str = "edge",
        translation_engine: str = "auto",
    ):
        """
        Initialize the video translator.

        Args:
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            device: 'auto', 'cuda', or 'cpu'
            tts_engine: 'edge' (faster, less voices) or 'coqui' (better quality)
            translation_engine: 'auto', 'libre', 'argo', or 'google'
        """
        self.whisper_model = whisper_model
        self.device = self._detect_device() if device == "auto" else device
        self.tts_engine = tts_engine
        self.translation_engine = translation_engine

        print(f"Video Translator initialized:")
        print(f"  Whisper model: {whisper_model}")
        print(f"  Device: {self.device}")
        print(f"  TTS engine: {tts_engine}")
        print(f"  Translation engine: {translation_engine}")

    def _detect_device(self) -> str:
        """Detect if CUDA is available."""
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
        except ImportError:
            pass
        return "cpu"

    def extract_audio(self, video_path: str, output_path: str) -> str:
        """Extract audio from video file."""
        print(f"\n[1/5] Extracting audio from video...")
        try:
            from moviepy.editor import VideoFileClip
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(output_path, verbose=False, logger=None)
            video.close()
            print(f"✓ Audio extracted: {output_path}")
            return output_path
        except ImportError:
            print("Error: moviepy not installed. Run: pip install moviepy")
            raise

    def transcribe(self, audio_path: str) -> Tuple[str, str]:
        """Transcribe audio to text using Whisper."""
        print(f"\n[2/5] Transcribing audio with Whisper ({self.whisper_model})...")

        try:
            import whisper
        except ImportError:
            print("Installing whisper...")
            subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"], check=True)
            import whisper

        model = whisper.load_model(self.whisper_model, device=self.device)
        result = model.transcribe(audio_path, word_timestamps=True)

        text = result["text"]
        detected_lang = result["language"]

        print(f"✓ Transcription complete")
        print(f"  Detected language: {detected_lang}")
        print(f"  Text length: {len(text)} characters")

        return text, detected_lang

    def translate(self, text: str, target_lang: str, source_lang: str = None) -> str:
        """Translate text to target language."""
        print(f"\n[3/5] Translating to {target_lang}...")

        # Language code mapping
        lang_map = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'tr': 'Turkish', 'pl': 'Polish', 'nl': 'Dutch', 'sv': 'Swedish',
            'da': 'Danish', 'fi': 'Finnish', 'no': 'Norwegian', 'el': 'Greek',
            'he': 'Hebrew', 'th': 'Thai', 'vi': 'Vietnamese', 'id': 'Indonesian',
            'ms': 'Malay', 'uk': 'Ukrainian', 'cs': 'Czech', 'ro': 'Romanian',
            'hu': 'Hungarian', 'bn': 'Bengali', 'ta': 'Tamil', 'te': 'Telugu',
            'mr': 'Marathi', 'ur': 'Urdu', 'fa': 'Persian', 'sw': 'Swahili',
        }

        target_name = lang_map.get(target_lang, target_lang)

        # Try different translation engines
        translated = None

        # 1. Try LibreTranslate (local or API)
        if self.translation_engine in ["auto", "libre"]:
            try:
                from libretranslatepy import LibreTranslateAPI
                # Try local instance first
                api = LibreTranslateAPI("http://localhost:5000")
                translated = api.translate(text, source_lang or "auto", target_lang)
                print(f"✓ Translated using LibreTranslate")
                return translated
            except:
                try:
                    # Try public API (may have limits)
                    api = LibreTranslateAPI("https://libretranslate.com")
                    translated = api.translate(text, source_lang or "auto", target_lang)
                    print(f"✓ Translated using LibreTranslate (public API)")
                    return translated
                except:
                    pass

        # 2. Try Argos Translate
        if self.translation_engine in ["auto", "argo"]:
            try:
                import argostranslate.package
                import argostranslate.translate

                # Download translation package if needed
                from_code = source_lang or "en"
                to_code = target_lang

                argostranslate.package.update_package_index()
                available_packages = argostranslate.package.get_available_packages()
                package = next(
                    (p for p in available_packages if p.from_code == from_code and p.to_code == to_code),
                    None
                )

                if package:
                    argostranslate.package.install_package(package)
                    translated = argostranslate.translate.translate(text, from_code, to_code)
                    print(f"✓ Translated using Argos Translate")
                    return translated
            except:
                pass

        # 3. Try Google Translate (via translatepy)
        if self.translation_engine in ["auto", "google"]:
            try:
                from translatepy import Translator
                translator = Translator()
                result = translator.translate(text, target_lang, source_lang)
                translated = result.result
                print(f"✓ Translated using Google Translate")
                return translated
            except:
                pass

        # 4. Fallback: Simple placeholder
        if translated is None:
            print("⚠ Translation failed, using original text")
            print("  Install translation engine: pip install libretranslatepy argostranslate")
            translated = text

        return translated

    def text_to_speech(self, text: str, lang: str, output_path: str) -> str:
        """Convert text to speech."""
        print(f"\n[4/5] Generating audio with {self.tts_engine} TTS...")

        if self.tts_engine == "edge":
            return self._tts_edge(text, lang, output_path)
        else:
            return self._tts_coqui(text, lang, output_path)

    def _tts_edge(self, text: str, lang: str, output_path: str) -> str:
        """Use Edge TTS (Microsoft's free TTS)."""
        try:
            import edge_tts
        except ImportError:
            print("Installing edge-tts...")
            subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"], check=True)
            import edge_tts

        # Language to voice mapping
        voice_map = {
            'en': 'en-US-AriaNeural', 'es': 'es-ES-ElviraNeural',
            'fr': 'fr-FR-DeniseNeural', 'de': 'de-DE-KatjaNeural',
            'it': 'it-IT-ElsaNeural', 'pt': 'pt-BR-FranciscaNeural',
            'ru': 'ru-RU-SvetlanaNeural', 'ja': 'ja-JP-NanamiNeural',
            'ko': 'ko-KR-SunHiNeural', 'zh': 'zh-CN-XiaoxiaoNeural',
            'ar': 'ar-SA-ZariyahNeural', 'hi': 'hi-IN-SwaraNeural',
            'tr': 'tr-TR-EmelNeural', 'pl': 'pl-PL-ZofiaNeural',
            'nl': 'nl-NL-ColetteNeural', 'sv': 'sv-SE-SofieNeural',
            'da': 'da-DK-ChristelNeural', 'fi': 'fi-FI-SelmaNeural',
            'no': 'no-NO-PernilleNeural', 'el': 'el-GR-AthinaNeural',
            'he': 'he-IL-HilaNeural', 'th': 'th-TH-PremwadeeNeural',
            'vi': 'vi-VN-HoaiMyNeural', 'id': 'id-ID-GadisNeural',
            'ms': 'ms-MY-YasminNeural', 'uk': 'uk-UA-PolinaNeural',
            'cs': 'cs-CZ-VlastaNeural', 'ro': 'ro-RO-AlinaNeural',
            'hu': 'hu-HU-NoemiNeural', 'bn': 'bn-BD-TanishaNeural',
            'ta': 'ta-IN-PallaviNeural', 'te': 'te-IN-ShrutiNeural',
            'mr': 'mr-IN-SwapnilNeural', 'ur': 'ur-PK-UzmaNeural',
            'fa': 'fa-IR-DilaraNeural', 'sw': 'sw-KE-ZuriNeural',
        }

        voice = voice_map.get(lang, 'en-US-AriaNeural')

        communicate = edge_tts.Communicate(text, voice)
        communicate.save(output_path)

        print(f"✓ Audio generated: {output_path}")
        return output_path

    def _tts_coqui(self, text: str, lang: str, output_path: str) -> str:
        """Use Coqui TTS (better quality, slower)."""
        try:
            from TTS.api import TTS
        except ImportError:
            print("Installing TTS...")
            subprocess.run([sys.executable, "-m", "pip", "install", "TTS"], check=True)
            from TTS.api import TTS

        # Use a multilingual model
        device = "cuda" if self.device == "cuda" else "cpu"
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        # Generate speech
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            language=lang,
        )

        print(f"✓ Audio generated: {output_path}")
        return output_path

    def merge_audio_video(self, video_path: str, audio_path: str, output_path: str):
        """Merge new audio with original video."""
        print(f"\n[5/5] Merging audio with video...")

        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
        except ImportError:
            print("Error: moviepy not installed")
            raise

        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Adjust video length to match audio
        if audio.duration > video.duration:
            # Loop video if audio is longer
            video = video.loop(duration=audio.duration)
        else:
            # Trim audio if video is longer
            audio = audio.subclip(0, video.duration)

        final_video = video.set_audio(audio)
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )

        video.close()
        audio.close()
        final_video.close()

        print(f"✓ Video saved: {output_path}")

    def translate_video(
        self,
        input_path: str,
        target_lang: str,
        output_path: Optional[str] = None,
        keep_temp: bool = False,
    ) -> str:
        """
        Full video translation pipeline.

        Args:
            input_path: Input video file path
            target_lang: Target language code (e.g., 'es', 'fr', 'de')
            output_path: Output video file path (default: input_translated.mp4)
            keep_temp: Keep temporary files

        Returns:
            Path to output video
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input video not found: {input_path}")

        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_translated_{target_lang}.mp4"

        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix="video_translator_"))

        try:
            # Step 1: Extract audio
            audio_path = temp_dir / "original_audio.wav"
            self.extract_audio(str(input_path), str(audio_path))

            # Step 2: Transcribe
            text, source_lang = self.transcribe(str(audio_path))

            # Step 3: Translate
            translated_text = self.translate(text, target_lang, source_lang)

            # Save translation
            translation_file = temp_dir / "translation.txt"
            with open(translation_file, "w", encoding="utf-8") as f:
                f.write(f"Original ({source_lang}):\n{text}\n\n")
                f.write(f"Translated ({target_lang}):\n{translated_text}")

            # Step 4: Text-to-speech
            new_audio_path = temp_dir / "translated_audio.wav"
            self.text_to_speech(translated_text, target_lang, str(new_audio_path))

            # Step 5: Merge
            self.merge_audio_video(str(input_path), str(new_audio_path), str(output_path))

            print(f"\n{'='*50}")
            print(f"✓ Translation complete!")
            print(f"  Output: {output_path}")
            print(f"{'='*50}")

            return str(output_path)

        finally:
            # Clean up temp files
            if not keep_temp:
                shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(
        description="Free Video Translator - Translate videos to any language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate to Spanish
  python video_translator.py input.mp4 --target-lang es

  # Translate to French with better quality
  python video_translator.py input.mp4 --target-lang fr --whisper-model small --tts coqui

  # Use GPU acceleration
  python video_translator.py input.mp4 --target-lang de --device cuda

Supported languages:
  en (English), es (Spanish), fr (French), de (German), it (Italian),
  pt (Portuguese), ru (Russian), ja (Japanese), ko (Korean), zh (Chinese),
  ar (Arabic), hi (Hindi), tr (Turkish), pl (Polish), nl (Dutch),
  sv (Swedish), da (Danish), fi (Finnish), no (Norwegian), el (Greek),
  he (Hebrew), th (Thai), vi (Vietnamese), id (Indonesian), ms (Malay),
  uk (Ukrainian), cs (Czech), ro (Romanian), hu (Hungarian), bn (Bengali),
  ta (Tamil), te (Telugu), mr (Marathi), ur (Urdu), fa (Persian), sw (Swahili)
        """
    )

    parser.add_argument("input", help="Input video file path")
    parser.add_argument("--target-lang", "-t", required=True,
                        help="Target language code (e.g., es, fr, de)")
    parser.add_argument("--output", "-o", help="Output video file path")
    parser.add_argument("--whisper-model", "-m", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--device", "-d", default="auto",
                        choices=["auto", "cuda", "cpu"],
                        help="Device to use (default: auto)")
    parser.add_argument("--tts-engine", default="edge",
                        choices=["edge", "coqui"],
                        help="TTS engine (default: edge)")
    parser.add_argument("--translation-engine", default="auto",
                        choices=["auto", "libre", "argo", "google"],
                        help="Translation engine (default: auto)")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep temporary files for debugging")

    args = parser.parse_args()

    # Create translator
    translator = VideoTranslator(
        whisper_model=args.whisper_model,
        device=args.device,
        tts_engine=args.tts_engine,
        translation_engine=args.translation_engine,
    )

    # Translate video
    try:
        translator.translate_video(
            input_path=args.input,
            target_lang=args.target_lang,
            output_path=args.output,
            keep_temp=args.keep_temp,
        )
    except KeyboardInterrupt:
        print("\nTranslation cancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
