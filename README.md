# symbol_creator

symbol_creator is a simple tool allowing you to create Inkscape symbol libraries from multiple svg files. The tool does nothing to validate the xml/svg data, but simple extracts all ```<path>``` elements from svg files and adds them to ```<symbol>``` elements.

# Usage

An example usage is below. This example recurses through the ```raw_lib``` directory, filters filenames with the regex, (in this example choosing only files with the word flat in them) and outputs it to the file called ```symlib.svg```. It also uses a yaml file to include the metadata which is explained below.

```python library.py --filter '.*[Ff]lat.*svg' --output symlib.svg --directory raw_lib --metadata example.yaml```

# Metadata
Simple metadata is supplied through the use of command line options to change the ```title```, ```license```, ```description```, ```author``` and ```language``` of the library. These are the only options supported by the supplied ```base.svg``` file. These options can also be supplied by using the ```--metadata``` option and pointing to a file which will have contents similar to the following.

```
author: Anon
language: English
description: A symbol library
title: Symbol Library
license: GPL
```

If customization of the ```base.svg``` is required, any other metadata fields may be added by using the ```##key###``` syntax, examples of which can be found in the supplied ```base.svg``` file.

# Future Work
Convert the creation of the file from ElementTree to Jinja2 templating.