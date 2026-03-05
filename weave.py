#!/usr/bin/env python3

"""
Python tool to convert a md file to html file :3
"""

VERSION = "1.0.0"

import argparse
from pathlib import Path
import requests

INDENT: str = " " * 4
NL: str = "\n"


def main() -> None:
    
    try:
        import requests
    except ImportError:
        print("[WEAVE]: 'requests' is required for --update")
        print("[WEAVE]: import it with `pip install requests`.")
        exit(1)
    
    parser = argparse.ArgumentParser(
        description="Convert a Markdown (.md) file into an HTML file.",
        epilog="""
        Example usage:
        python weave.py README.md
        python weave.py notes.md -o notes.html
        python weave.py doc.md -d build -o index.html
        """
    )

    parser.add_argument(
        "filepath",
        nargs="?",
        help="Path to the Markdown (.md) file to convert"
    )

    parser.add_argument(
        "-d", "--output-dir",
        default=".",
        help="Directory where HTML file will be saved (default: current dir)"
    )

    parser.add_argument(
        "-o", "--output-file-name",
        default="index.html",
        help="Name of new HTML file (default: index.html)"
    )
    
    parser.add_argument(
        "--version", "-v", 
        action="version", 
        version=f"Weave {VERSION}")
    
    parser.add_argument(
        "--update", 
        action="store_true",
        help="Update to the latest version"
     )

    args = parser.parse_args()

    if args.update:
        update_program()
        return

    if not args.filepath:
        parser.error("[WEAVE]: Filepath required unless using --update")

    parse(args.filepath, args.output_dir, args.output_file_name)


def get_latest_release():
	LATEST_RELEASE_URL = "https://api.github.com/repos/kayym33/weave/releases/latest"
	response = requests.get(LATEST_RELEASE_URL, timeout=10)
	data = response.json()
	return data["tag_name"], data["assets"][0]["browser_download_url"]


def download_url_file(url, path):
	response = requests.get(url, timeout=10)
	with open(path, "wb") as file_writer:
		file_writer.write(response.content)


def update_program():
	latest_version, download_url = get_latest_release()
	latest_version = latest_version.lstrip("v")

	if latest_version == VERSION:
		print("[WEAVE]: Already up to date.")
		return

	print(f"[WEAVE]: Updating to {latest_version}...")

	download_url_file(download_url, "weave_new")

	import os, sys
	os.replace("weave_new", sys.argv[0])

	print("[WEAVE]: Update complete.")


def parse(filepath: str, output_dir: str, output_file_name: str) -> None:
    output: str = ""
    in_list: bool = False

    with open(filepath, encoding="utf-8") as md_file:
        for line in md_file:
            line = line.rstrip("\n")

            if line.strip() == "":
                continue

            if line.startswith("#"):
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                hash_count = 0
                for char in line:
                    if char == "#":
                        hash_count += 1
                    else:
                        break

                # if > 6 default to max (<h6>)
                if hash_count > 6:
                    hash_count = 6

                text = line[hash_count:].strip()
                output += f"<h{hash_count}>{text}</h{hash_count}>{NL}"

            elif line.startswith("- "):
                if not in_list:
                    output += "<ul>" + NL
                    in_list = True

                output += f"{INDENT}<li>{line[2:]}</li>{NL}"

            elif line.startswith("`"):
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                code_text = line.strip("`")
                output += f"<p><code>{code_text}</code></p>{NL}"

            elif set(line.strip()) == {"*"} and len(line.strip()) >= 3:
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                output += "<hr />" + NL

            elif line.startswith("> "):
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                output += f"<blockquote>{line[2:]}</blockquote>{NL}"

            else:
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                parsed_line = parse_inline(line)
                output += f"<p>{parsed_line}</p>{NL}"


    output_to_file(output, output_dir, output_file_name)


def parse_inline(line: str) -> str:
    result = ""
    i = 0

    italic = False
    bold = False

    while i < len(line):
        if line[i] == "*":
            count = 0
            while i < len(line) and line[i] == "*":
                count += 1
                i += 1

            if count == 3:
                if bold and italic:
                    result += "</em></strong>"
                    bold = italic = False
                else:
                    result += "<strong><em>"
                    bold = italic = True

            elif count == 2:
                if bold:
                    result += "</strong>"
                else:
                    result += "<strong>"
                bold = not bold

            elif count == 1:
                if italic:
                    result += "</em>"
                else:
                    result += "<em>"
                italic = not italic

        else:
            result += line[i]
            i += 1

    return result


def output_to_file(output: str, output_dir: str, output_file_name: str) -> None:

    # build output path
    output_path = Path(output_dir) / output_file_name

    # create dir if not exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as fw:
        fw.write(output)

if __name__ == '__main__':
    main()


#TODO
# ![alt text](image_url) -> <img src="image_url" alt="alt text">
