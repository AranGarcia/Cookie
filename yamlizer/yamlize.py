import sys

from handler import LegalFileStructure
from items import identify_item

# Input argument: file to be parsed
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage\n\tyamlize.py FILE [OUTPUT_FILE]\n", file=sys.stderr)
    exit(1)

fname = sys.argv[1]
lfs = LegalFileStructure()
with open(fname) as input_file:
    for line in input_file:
        item = identify_item(line)
        if item:
            lfs.add_item(item)

if len(sys.argv) == 3:
    outfile = sys.argv[2]
    if not outfile.endswith(".yaml"):
        outfile += ".yaml"
else:
    outfile = "result.yaml"
lfs.write_file(outfile)