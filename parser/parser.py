from writer.writer import output_to_file
from constants.constants import INDENT, NL

def parse(filepath: str, output_dir: str, output_file_name: str) -> None:
    """Read a Markdown file, convert it to HTML, and write it to disk."""
    with open(filepath, encoding="utf-8") as md_file:
        content = md_file.read()

    output = parse_string(content)
    output_to_file(output, output_dir, output_file_name)


def parse_string(content: str) -> str:
    """Convert a Markdown string to an HTML string."""
    output: str = ""
    in_list: bool = False

    for line in content.splitlines():
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

    if in_list:
        output += "</ul>" + NL

    return output


def parse_inline(line: str) -> str:
    """Convert inline Markdown formatting (bold, italic) to HTML."""
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
