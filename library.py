import argparse
import os
import os.path
import re
import yaml

from symlib import SymbolLibrary

parser = argparse.ArgumentParser(argument_default=None)

interaction = parser.add_argument_group('Main Options')
interaction.add_argument('--directory',
                         help="Directory containing SVG files",
                         default="library")
interaction.add_argument('--output',
                         help="Directory containing SVG files",
                         default="output.svg")
interaction.add_argument('--filter',
                         help="Filter the filenames with regex match",
                         default=None)
interaction.add_argument('--metadata',
                         help="A yaml file containing default metadata",
                         default=None)
interaction.add_argument('--base',
                         help="The base template file",
                         default='base.svg')

mdata = parser.add_argument_group('Metadata')
mdata.add_argument('--title',
                   help="Title of Library",
                   default="Symbol Library")
mdata.add_argument('--description',
                   help="Description of Library",
                   default="A symbol library")
mdata.add_argument('--author',
                   help="The Author of the library",
                   default="Anon")
mdata.add_argument('--language',
                   help="The Language of the library",
                   default="English")
mdata.add_argument('--license',
                   help="The License of the library",
                   default="GPL")
args = vars(parser.parse_args())


# Make us some nice counters for errors and conversions
c = 0
e = 0

# Iterate the files in the "library" dir
files = [os.path.join(d, fn) for d, dn, fns in os.walk(args['directory']) for fn in fns]


if args['metadata']:
    metadata = yaml.load(open(args['metadata']))
else:
    metadata = args

symlib = SymbolLibrary(args['output'], base=args['base'], metadata=metadata)

for filename in files:
    # Only process '.svg' files
    if '.svg' in filename:
        if args['filter']:
            if not re.match(args['filter'], filename):
                continue
            try:
                symlib.add_file(filename)
                c += 1
            except:
                e += 1
                continue

print "Successfully converted {} out of {} files".format(c, e + c)

symlib.write_library()
