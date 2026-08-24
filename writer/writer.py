from pathlib import Path

from constants.constants import *

def output_to_file(output: str, output_dir: str, output_file_name: str) -> None:

    # build output path
    output_path = Path(output_dir) / output_file_name

    # create dir if not exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as fw:
        fw.write(output)