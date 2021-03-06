"""
Preprocessing script that transforms Shepard unstructured legal TXT files from
unstructured TXT to a YAML format.
"""
import sys

from handler import LegalFileStructure
from items import identify_item

# Input argument: file to be parsed
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage\n\tstructurize.py FILE [OUTPUT_FILE]\n", file=sys.stderr)
    exit(1)

fname = sys.argv[1]
lfs = LegalFileStructure()
paragraphs = []
with open(fname) as input_file:
    for line in input_file:
        # Remove trailing whitespace.
        line = line.strip()

        # Parse all paragraphs as a single item
        if line != "":
            paragraphs.append(line)
        else:
            text = "\n".join(paragraphs)
            paragraphs.clear()
            item = identify_item(text)
            if item:
                lfs.add_item(item)

if len(sys.argv) < 3:
    outfile = "result"
else:
    outfile = sys.argv[2]
lfs.write_file(outfile, file_format="json")
