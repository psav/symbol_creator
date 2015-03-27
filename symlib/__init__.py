import xml.etree.ElementTree as ET
import os.path
import re


class SymbolLibrary(object):

    # Create a base template object for the "symbol"
    template = """<symbol id="">
    <title></title>
    </symbol>"""

    def __init__(self, filename, base="base.svg", title="Symbol Library",
                 description="A symbol library", author="Anon"):

        self.filename = filename

        # Create the container for the symbols
        self.dtree = ET.fromstring("<defs></defs>")

        # Create the base svg file

        with open(base) as f:
            base_svg = f.read()
        if title:
            base_svg = base_svg.replace("##title##", title)
        if description:
            base_svg = base_svg.replace("##description##", description)
        if author:
            base_svg = base_svg.replace("##author##", author)

        self.broot = ET.fromstring(base_svg)

        self.symbol_name = {}

    def name_gen(self, name, num=0):
        if name in self.symbol_name:
            self.name_gen(name, num + 1)
        else:
            return name

    def add_symbol(self, name, elems):
        for elem in elems:
            # Wrap the path in the base template
            ntree = ET.fromstring(self.template)
            ntree.set('id', name)
            ntree.find('title').text = name
            ntree.insert(1, elem)

            # Add the symbol to the 'defs'
            self.dtree.insert(1, ntree)

    def add_file(self, filename):
        name = self.name_gen(os.path.splitext(os.path.split(filename)[1])[0])

        # Find the root element
        try:
            tree = ET.parse(filename)
        except:
            raise Exception('This file could not be parsed')
        root = tree.getroot()

        # Fine _all_ the paths (hint: I only wanted one :( )
        elems = []
        for elem in root.iter():
            if elem.tag == '{http://www.w3.org/2000/svg}path':
                elems.append(elem)

        # If we find no elements raise an exception
        if len(elems) == 0:
            print "{} failed!".format(filename)
            raise Exception('This file has no elements')

        self.add_symbol(name, elems)

    def write_library(self):
        self.broot.insert(5, self.dtree)
        output = ET.tostring(self.broot)

        # Nasty hack to remove the ns0 namespace else inkscape doesn't like it
        xmlstring = re.sub('ns0:', '', output)

        # Write it out
        with open(self.filename, "w") as f:
            f.write(xmlstring)
