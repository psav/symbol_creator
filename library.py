import os
import os.path
import xml.etree.ElementTree as ET
import re

# Create a base template object for the "symbol"
template = """<symbol id="">
<title></title>
</symbol>"""

# Create the container for the symbols
dtree = ET.fromstring("<defs></defs>")

# Create the base svg file
btree = ET.parse('base.svg')
broot = btree.getroot()

# Make us some nice counters for errors and conversions
c = 0
e = 0

# Iterate the files in the "library" dir
files = os.listdir('library')
for filename in files:

    # Only process '.svg' files
    if 'svg' in filename:

        # Grab the name of the symbol from the filename
        name = os.path.splitext(filename)[0]

        # Find the root element
        tree = ET.parse(os.path.join('library', filename))
        root = tree.getroot()

        # Fine _all_ the paths (hint: I only wanted one :( )
        elem = root.findall('{http://www.w3.org/2000/svg}path')

        # If we find more than one continue and skip the file
        if len(elem) == 0:
            print "{} failed!".format(filename)
            e += 1
            continue
        else:
            c += 1
            elem = elem[0]

        # Wrap the path in the base template
        ntree = ET.fromstring(template)
        ntree.set('id', name)
        ntree.find('title').text = name
        ntree.insert(1, elem)

        # Add the symbol to the 'defs'
        dtree.insert(1, ntree)

# Add the 'defs' to the base.svg file
broot.insert(5, dtree)
output = ET.tostring(broot)

# Nasty hack to remove the ns0 namespace else inkscape doesn't like it
xmlstring = re.sub('ns0:', '', output)

# Write it out
with open('output.svg', "w") as f:
    f.write(xmlstring)

print "Parsed {} files, successfully converted {}".format(e + c, c)
