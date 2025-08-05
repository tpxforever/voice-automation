# Most basic script, converts text files to audio files with grammar correction
# Requirements: gTTS, language_tool_python, langdetect

import os
from pathlib import Path
from gtts import gTTS
import language_tool_python
from langdetect import detect

# Paths
input_folder = Path("InputFiles")
output_text_folder = Path("OutputFiles")
output_audio_folder = Path("OutputAudio")

# Ensure output folders exist
output_text_folder.mkdir(exist_ok=True)
output_audio_folder.mkdir(exist_ok=True)

# Load grammar tool
tool = language_tool_python.LanguageTool('en-US')

# Loop through all .txt files in input folder
for file in input_folder.glob("*.txt"):
    with open(file, 'r') as f:
        original_text = f.read()

    #Language Detection
    lang_code = detect(original_text)
    lang_map = {
    "en": "en-US",      # English (US)
    "zh-cn": "zh-CN",   # Chinese (Simplified)
    "ms": "id",          # Malay → mapped to Indonesian
    }

    lt_lang = lang_map.get(lang_code)
    if lt_lang:
        tool = language_tool_python.LanguageTool(lt_lang)
        corrected_text = tool.correct(original_text)
    else:
        print("Grammar correction not available.")
        corrected_text = original_text

    # Grammar check and correction
    corrected_text = tool.correct(original_text)

    # Save corrected text
    corrected_filename = output_text_folder / f"{file.stem}_corrected.txt"
    with open(corrected_filename, 'w') as f:
        f.write(corrected_text)

    # Convert to voice
    tts = gTTS(corrected_text)
    audio_filename = output_audio_folder / f"{file.stem}_audio.mp3"
    tts.save(audio_filename)

    print(f"Processed: {file.name}")
