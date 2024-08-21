import os

from from_epub import to_txt
from to_wav import to_wav
from to_mp3 import to_mp3


def convert():
    to_txt()
    to_wav()
    to_mp3()


if __name__ == "__main__":
    for folder in ["inputs", "txt", "wav", "mp3"]:
        os.makedirs(folder, exist_ok=True)
    convert()
