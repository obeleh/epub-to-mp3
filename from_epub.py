import os
import re
from os.path import join

import pandoc

from shared import get_files_in_folder


def clean_text(input_text):
    # Remove non-breaking spaces
    non_nbsp = input_text.replace('\xa0', ' ')

    # remove empty lines
    remove_spaces = re.sub(r'\n\s+\n', '\n\n', non_nbsp)
    while '\n\n\n' in remove_spaces:
        remove_spaces = remove_spaces.replace('\n\n\n', '\n\n')

    # Regular expression to find and remove all <span>...</span> elements but keep the text inside
    removed_spans = re.sub(r'<span[^>]*?>(.*?)</span>', r'\1', remove_spaces, flags=re.DOTALL)

    # Pattern to identify standalone newlines that should be removed
    # This will preserve paragraph breaks and remove only single newlines
    cleaned_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', removed_spans)
    return cleaned_text


def to_txt():
    for fl in get_files_in_folder("inputs"):
        fl = str(fl)
        fl_out = join("txt", fl.replace(".epub", ".txt"))
        if fl.endswith(".epub") and not os.path.isfile(fl_out):
            doc = pandoc.read(
                file=join("inputs", fl)
            )
            pandoc.write(
                doc,
                file=fl_out,
                format="plain",
            )
            with open(fl_out, "r") as f:
                contents = f.read()
            cleaned_text = clean_text(contents)
            with open(fl_out, "w") as f:
                f.write(cleaned_text)


if __name__ == "__main__":
    to_txt()