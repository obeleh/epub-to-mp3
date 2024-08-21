from os.path import join

from pydub import AudioSegment
from shared import get_files_in_folder


def collect_numbers(files):
    # files are number <title>.number.wav
    # collect the file numbers for each title
    numbers = {}
    for fl in files:
        if not fl.endswith(".wav"):
            continue
        parts = fl.rsplit(".", 2)
        title = parts[0]
        number = parts[1]
        if title not in numbers:
            numbers[title] = []
        numbers[title].append(number)
    return numbers


def to_mp3():
    for title, numbers in collect_numbers(get_files_in_folder("wav")).items():
        if "Eric" not in title:
            continue
        data = None
        for number in sorted(numbers):
            fl_in = join("wav", f"{title}.{number}.wav")
            print(fl_in)
            segment = AudioSegment.from_wav(fl_in)
            if data is None:
                data = segment
            else:
                data += segment
        data.export(join("mp3", f"{title}.mp3"), format="mp3")


if __name__ == "__main__":
    to_mp3()
