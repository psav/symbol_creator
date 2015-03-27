import argparse
import os
import os.path
import re
from symlib import SymbolLibrary

parser = argparse.ArgumentParser(argument_default=None)

interaction = parser.add_argument_group('Main Options')
interaction.add_argument('--directory',
                         help="Directory containing SVG files",
                         default=None)
interaction.add_argument('--output',
                         help="Directory containing SVG files",
                         default="output.svg")
interaction.add_argument('--filter',
                         help="Filter the filenames with regex match",
                         default=None)

metadata = parser.add_argument_group('Metadata')
metadata.add_argument('--title',
                      help="Title of Library",
                      default="Symbol Library")
metadata.add_argument('--description',
                      help="Description of Library",
                      default="A symbol library")
metadata.add_argument('--author',
                      help="The Author of the library",
                      default="Anon")
args = vars(parser.parse_args())

# Make us some nice counters for errors and conversions
c = 0
e = 0

# Iterate the files in the "library" dir
files = [os.path.join(d, fn) for d, dn, fns in os.walk('raw_lib') for fn in fns]


symlib = SymbolLibrary(args['output'], title=args['title'], description=args['description'],
                       author=args['author'])

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
