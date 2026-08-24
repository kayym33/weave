import argparse
from pathlib import Path
from constants.constants import VERSION
from updater.updater import update_program
from parser.parser import parse

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