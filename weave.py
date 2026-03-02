"""
Python tool to convert a md file to html file
"""
INDENT = (" " * 4)
NL = "\n"
# read in md file
filepath="file.md"
mdfile = open(filepath)
outputstr = ""

with open(filepath) as mdfile:
    for line in mdfile:
        line = line.rstrip("\n")
        
        if line.startswith("#"):
            hashcount = 0
            for char in line:
                if char == "#":
                    hashcount += 1
                else:
                    break
            text = line[hashcount:].strip()
            newline = f"<h{hashcount}>{text}</h{hashcount}>"
            outputstr += newline + NL    
        
        elif line.startswith("-"):
            newline = f"<li>{line[2:]}</li>"
            outputstr += newline + NL
        else:
            newline = f"<p>{line}</p>"
            outputstr += newline + NL


# output to html file
# random number just to test so i dont have to keep deleting the file if it already exists
import random
x = "newhtml" + str(random.randint(1111,9999)) 
htmlfile = f"{x}.html"

# create new file
with open(htmlfile, "a") as filewriter:
    filewriter.write(outputstr)
    
# print contents of file
with open(htmlfile) as filereader:
    print(filereader.read())

# preferably be able to do:
# - python weave.py "markdownfile.md" <- outputs file to same directory, default to same name as md file
# - python weave.py "markdownfile.md" --output-dir "outputdir" <- output to specific directory, default to same name as md file
# - python weave.py "markdownfile.md" --output-file-name "newfile.html" <- specify name of new html file


# all of them together
# python weave.py "markdownfile.md" --output-dir "/desktop" --ouput-file-name "index.html"
 
