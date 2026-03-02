"""
Python tool to convert a md file to html file
"""
INDENT=(" " * 4)
# read in md file
filepath="file.md"
mdfile = open(filepath)
outputstr = ""
nl = "\n"

for line in mdfile:
    line = line.rstrip("\n")
    if line.startswith("#"):
        hashcount = 0
        for char in line:
            if char == "#":
                hashcount += 1
        newline = f"<h{hashcount}>" + line[hashcount+1:] + f"<h{hashcount}>" 
        print(f"<h{hashcount}>" + line[hashcount+1:] + f"<h{hashcount}>")
        outputstr += str(f"<h{hashcount}>" + line[hashcount+1:] + f"<h{hashcount}>" + nl)
    
    elif line.startswith("-"):
        print("<lo>")
        print(INDENT +"<li>" + line[2:] + "<li>")
        print("<lo>\n")
    else:
        print("<p>" + line + "<p>")

# output to html file
import random

x = "newhtml" + str(random.randint(1111,9999))
htmlfile = open(str(f"{x}.html"), "x")

with open(str(htmlfile), "a") as filewriter:
    filewriter.write(outputstr)
    
with open(str(htmlfile)) as f:
    print(f.read())

# preferably be able to do:
# - python weave.py "markdownfile.md" <- outputs file to same directory, default to same name as md file
# - python weave.py "markdownfile.md" --output-dir "outputdir" <- output to specific directory, default to same name as md file
# - python weave.py "markdownfile.md" --output-file-name "newfile.html" <- specify name of new html file


# all of them together
# python weave.py "markdownfile.md" --output-dir "/desktop" --ouput-file-name "index.html"
 
