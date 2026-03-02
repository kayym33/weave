"""
Python tool to convert a md file to html file :3
"""

# important stuff 
import argparse
from pathlib import Path
INDENT: str = (" " * 4)
NL: str = "\n"

#TODO
# bold -> <strong>...</strong>
# italic -> <em>...</em>
# ![alt text](image_url) -> <img src="image_url" alt="alt text">
# > blockquote -> <blockquote>...</blockquote>
#TODO

def main() -> None:
    parser = argparse.ArgumentParser()
    
    # mandatory args:
    parser.add_argument("filepath")
    
    # optional args:
    parser.add_argument("--output-dir", "-d", default=".")
    parser.add_argument("--output-file-name", "-o", default="index.html")
    
    args = parser.parse_args()
    
    parse(args.filepath, args.output_dir, args.output_file_name)
    

def parse(filepath, output_dir, output_file_name) -> None:
    output: str = ""
    in_list: bool = False

    with open(filepath) as md_file:
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

                text = line[hash_count:].strip()
                output += f"<h{hash_count}>{text}</h{hash_count}>{NL}"

            elif line.startswith("-"):
                if not in_list:
                    output += "<ul>" + NL
                    in_list = True

                output += f"{INDENT}<li>{line[2:]}</li>{NL}"
                
            elif line.startswith("`"):
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                code_text = line.strip("`")
                output += f"<code>{code_text}</code>{NL}"

            elif set(line.strip()) == {"*"} and len(line.strip()) >= 3:
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                output += "<hr>" + NL

            else:
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                parsed_line = parse_inline(line)
                output += f"<p>{parsed_line}</p>{NL}"

                if in_list:
                    output += "</ul>" + NL
                
    output_to_file(output, output_dir, output_file_name)

def parse_inline(line):
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

def output_to_file(output, output_dir, output_file_name) -> None:
    
    # build output path
    output_path = Path(output_dir) / output_file_name
    
    # create dir if not exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as fw:
        fw.write(output)
        
        
if __name__ == '__main__':
    main()
