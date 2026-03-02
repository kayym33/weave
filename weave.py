"""
Python tool to convert a md file to html file :3
"""

# important stuff 
import argparse
from pathlib import Path
INDENT = (" " * 4)
NL = "\n"


def main():
    
    parser = argparse.ArgumentParser()
    
    # mandatory args:
    parser.add_argument("filepath")
    
    # optional args:
    parser.add_argument("--output-dir", "-d", default=".")
    parser.add_argument("--output-file-name", "-o", default="index.html")
    
    args = parser.parse_args()
    
    parse(args.filepath, args.output_dir, args.output_file_name)
    

def parse(filepath, output_dir, output_file_name):
    output = ""
    in_list = False
    NL = "\n"

    with open(filepath) as md_file:
        for line in md_file:
            line = line.rstrip("\n")

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
                new_line = f"<h{hash_count}>{text}</h{hash_count}>"
                output += new_line + NL

            elif line.startswith("-"):
                if not in_list:
                    output += "<ul>" + NL
                    in_list = True

                new_line = f"{INDENT}<li>{line[2:]}</li>"
                output += new_line + NL

            else:
                if in_list:
                    output += "</ul>" + NL
                    in_list = False

                new_line = f"<p>{line}</p>"
                output += new_line + NL

    if in_list:
        output += "</ul>" + NL
                
    outputtofile(output, output_dir, output_file_name)


def outputtofile(output, output_dir, output_file_name):
    
    # build output path
    output_path = Path(output_dir) / output_file_name
    
    # create dir if not exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as fw:
        fw.write(output)
        
        
if __name__ == '__main__':
    main()
