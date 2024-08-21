import os
import re
from os.path import join
from shared import get_files_in_folder


# Split text into chunks of 3000 characters by splitting at newlines
def chunk_text_lines_simple(text, max_chunk_size=250):
    chunk = ""
    for line in text.split("\n"):
        if len(chunk) + len(line) < max_chunk_size:
            chunk += line + "\n"
        else:
            stripped = chunk.strip()
            if stripped:
                yield stripped
            chunk = line + "\n"
    yield chunk


def chunk_text_lines_no_punctuation(text, max_chunk_size=250):
    chunk = ""
    for line in text.split("\n"):
        if len(line) > max_chunk_size:
            sentences = line.split('.')
            for sentence in sentences:
                if len(chunk) + len(sentence) + 1 < max_chunk_size:
                    chunk += sentence + '.'
                else:
                    if chunk:
                        yield chunk
                    chunk = sentence + '.'  # Start new chunk directly with the sentence
        else:
            if len(chunk) + len(line) < max_chunk_size:
                chunk += line + "\n"
            else:
                if chunk:
                    yield chunk
                chunk = line + "\n"  # Start new chunk directly with the line

    if chunk:
        yield chunk


def chunk_text_lines(text, max_chunk_size=250):
    chunk = ""
    for line in text.split("\n"):
        if len(line) > max_chunk_size:
            # Split sentences by both '.' and '?', retaining the delimiter
            sentences = re.split(r'([,.?\n])', line)
            sentence_accumulator = ""
            for part in sentences:
                if part in ',.?\n':
                    sentence_accumulator += part  # Append the delimiter to the current sentence
                    if len(chunk) + len(sentence_accumulator) < max_chunk_size:
                        chunk += sentence_accumulator
                    else:
                        if chunk:
                            yield chunk.lstrip()
                        chunk = sentence_accumulator
                    sentence_accumulator = ""  # Reset for the next sentence
                else:
                    sentence_accumulator += part  # Append non-delimiter text
        else:
            if len(chunk) + len(line) < max_chunk_size:
                chunk += line + "\n"
            else:
                if chunk:
                    yield chunk.lstrip()
                chunk = line + "\n"  # Start new chunk directly with the line

    if chunk:
        yield chunk.lstrip()


def to_wav():
    from TTS.api import TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    for fl in get_files_in_folder("txt"):
        fl = str(fl)
        print(fl)
        if fl.endswith(".txt"):
            text = open(join("txt", fl), "r").read()
            for idx, chunk in enumerate(chunk_text_lines(text)):
                idx = str(idx).zfill(4)
                out_fl = join("wav", fl.replace(".txt", f".{idx}.wav"))
                if not os.path.isfile(out_fl):
                    tts.tts_to_file(
                        text=chunk,
                        file_path=out_fl,
                        speaker="Annmarie Nele",
                        speed=1.3,
                        language="en",
                        split_sentences=False,
                    )


if __name__ == "__main__":
    to_wav()